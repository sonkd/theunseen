module Jekyll
    class AggregatePostsAndPages < Generator
      safe true
  
      def generate(site)
        # Combine posts and pages into a single array
        site.config['posts_and_pages'] = (site.posts.docs + site.pages).sort_by { |item| item.data['title'] || item.data['date'] || item.name }
      end
    end
  end