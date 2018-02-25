FROM ruby:2.5.0
ADD . /sinatra
WORKDIR /sinatra
COPY Gemfile /sinatra/
RUN bundle install --quiet
COPY . /sinatra
CMD ["ruby", "run.rb"]
