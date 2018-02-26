FROM ruby:2.5.0
RUN mkdir -p /app
WORKDIR /app
COPY Gemfile /app/
RUN bundle install --quiet
COPY . /app
EXPOSE 5001
CMD ["bundle", "exec", "rackup", "--host", "0.0.0.0", "-p", "5001"]
