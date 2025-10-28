module Jekyll
  module ReadingTime
    WORDS_PER_MINUTE = 200.0

    def reading_time(input)
      words = strip_html(input.to_s).split.size
      minutes = (words / WORDS_PER_MINUTE).ceil
      "#{minutes}분 소요"
    end
  end
end

Liquid::Template.register_filter(Jekyll::ReadingTime)
