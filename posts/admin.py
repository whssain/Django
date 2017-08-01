from .models import Post
from django.contrib import admin
admin.site.register(Post) 


class TutrModelAdmin(admin.ModelAdmin):
	
	list_display = ["title", "timestamp", "updated"]
	search_fields = ["title", "content"]
	list_filter = ["timestamp"]
    
	list_display_links = ['timestamp']
	list_editable = ["title"]
	class Meta:
		model = Post






