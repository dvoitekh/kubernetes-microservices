require 'bundler'; Bundler.require

Dotenv.load

require './utils'
require './mongoid'

class App < Sinatra::Base
  set :bind, '0.0.0.0'
  set :port, ENV['APP_PORT']

  before do
    content_type :json
    request.body.rewind
    body_str = request.body.read
    @request_payload = body_str.empty? ? {} : JSON.parse(body_str)
  end

  def login_params
    params = @request_payload.slice('username', 'password')
    halt 422, { error: 'Invalid credentials' }.to_json if params.count < 2 || params['password'].length < 6
    params['password'] = Utils.hmac_signature(params['password'])
    params
  end

  def user_params
    login_params.merge(id: User.count + 1, created_at: Time.now)
  end

  post '/users' do
    begin
      user = User.create!(user_params)
      user.to_json
    rescue Mongoid::Errors::Validations
      halt 422, { error: 'Username already exists' }.to_json
    end
  end

  post '/login' do
    begin
      user = User.find_by(login_params)
      { token: Utils::JsonWebToken.encode(user_id: user.id) }.to_json
    rescue Mongoid::Errors::DocumentNotFound, Mongo::Error::OperationFailure
      halt 404, { error: 'Invalid username or password' }.to_json
    end
  end

  get '/check_login' do
    http_token = request.env['HTTP_AUTHORIZATION']&.split(' ')&.last
    begin
      auth_token = Utils::JsonWebToken.decode(http_token.to_s)
      auth_token.to_json
    rescue JWT::VerificationError, JWT::DecodeError, JWT::ExpiredSignature
      halt 401, { error: 'User is unauthorized' }.to_json
    end
  end
end
