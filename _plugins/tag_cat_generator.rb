module Jekyll
  class TagCategoryGenerator < Generator
    def generate(site)
      all_docs = site.collections.flat_map { |_, coll| coll.docs }
      site.data['all_tags'] = {}
      # Lấy danh sách category định nghĩa sẵn
      defined_cats = site.data['categories']&.map { |c| c['name'] } || []
      site.data['all_categories'] = {}
      site.data['category_meta'] = {}

      # Tạo lookup table từ slug sang category name
      cat_lookup = {}
      site.data['categories']&.each do |cat|
        cat_lookup[cat['slug']] = cat['name']
        site.data['category_meta'][cat['name']] = cat
      end
      
      all_docs.each do |doc|
        # Xử lý tags
        if tags = doc.data['tags']
          tags.each do |tag|
            site.data['all_tags'][tag] ||= []
            site.data['all_tags'][tag] << doc
          end
        end
        
        # Xử lý categories
        if categories = doc.data['categories']
          categories.each do |category|
            site.data['all_categories'][category] ||= []
            site.data['all_categories'][category] << doc
          end
        end
      end
    end
  end
end