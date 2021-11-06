from django.urls import path
from . import views
from .reactviews.editpost import postimages as imageViews 
from .reactviews.editpost import postbasics as postViews 
from .reactviews.editpost import postselect as postSelectViews
from .reactviews.editpost import statusactive as statusActiveViews
from .reactviews.editpost import postlink as postLinkViews

#Both
urlpatterns = [
    path("get_categories/", views.BackAndFront.get_categories, name="get_categories"),

 
]

#Back
#Images
urlpatterns += [
    path("get_available_images", imageViews.get_available_images, name="get_available_images"),
    path("add_or_remove_post_image", imageViews.add_or_remove_post_image, name="add_or_remove_post_image"),
    path("set_main_image", imageViews.set_main_image, name="set_main_image"),
]
#Posts
urlpatterns += [
    path("get_post_choices/", views.BackOnly.get_post_choices, name="get_post_choices"),#
    path("toggle_post_active/", views.BackOnly.toggle_post_active, name="toggle_post_active"),
    path("edit_post_basics/", views.BackOnly.edit_post_basics, name="edit_post_basics"),
    
    path("change_template_or_category", postSelectViews.change_template_or_category, name="change_template_or_category"),


]

urlpatterns += [
    path("add_new_link", postLinkViews.add_new_link, name="add_new_link"),
    path("remove_link_from_post", postLinkViews.remove_link_from_post, name="remove_link_from_post"),
    path("get_available_links", postLinkViews.get_available_links, name="get_available_links"),
    path("add_link_to_post", postLinkViews.add_link_to_post, name="add_link_to_post"),
    path("get_post_links", postLinkViews.get_post_links, name="get_post_links"),
]