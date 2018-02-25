require 'mongoid'

Mongoid.load!('config/mongoid.yml')

class User
  include Mongoid::Document

  field :username, type: String
  field :password, type: String
  field :created_at, type: Time

  validates_uniqueness_of :username
end
