require 'openssl'

module Utils
  class JsonWebToken
    def self.encode(payload)
      exp = Time.now.to_i + ENV['AUTH_TOKEN_LIFETIME'].to_i
      JWT.encode(payload.merge(exp: exp), ENV['SECRET_KEY'], 'HS256')
    end

    def self.decode(token)
      JWT.decode(token, ENV['SECRET_KEY'], true, algorithm: 'HS256')[0]
    end
  end

  def self.hmac_signature(payload)
    digest = OpenSSL::Digest.new('sha1')
    OpenSSL::HMAC.hexdigest(digest, ENV['SECRET_KEY'], payload.to_s)
  end
end
