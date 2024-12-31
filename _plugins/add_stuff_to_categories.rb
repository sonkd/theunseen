module Jekyll
    class AddStuffToCategories < Generator
      safe true
  
      def generate(site)
        site.collections['stuff'].docs.each do |doc|
          next unless doc.data['categories'] # Skip items without categories
  
          doc.data['categories'].each do |category|
            site.categories[category] ||= [] # Initialize category array if it doesn't exist
            site.categories[category] << doc # Add the document to the category
          end
        end
      end
    end
end
  