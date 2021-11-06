from django.urls import path
from . import views


#Both
urlpatterns = [
    path("get_categories/", views.BackAndFront.get_categories, name="get_categories"),
]

#Back
#Posts
urlpatterns += [
    path("get_post_choices/", views.BackOnly.get_post_choices, name="get_post_choices"),#
    path("toggle_post_active/", views.BackOnly.toggle_post_active, name="toggle_post_active"),
    path("edit_post_basics/", views.BackOnly.edit_post_basics, name="edit_post_basics"),
    path("change_template_or_category/", views.BackOnly.change_template_or_category, name="change_template_or_category"),
]

#Images
urlpatterns += [
    path("get_available_images/", views.BackOnly.get_available_images, name="get_available_images"),
    path("add_or_remove_post_image/", views.BackOnly.add_or_remove_post_image, name="add_or_remove_post_image"),
    path("set_main_image/", views.BackOnly.set_main_image, name="set_main_image"),
]

#Links
urlpatterns += [
    path("add_new_link/", views.BackOnly.add_new_link, name="add_new_link"),
    path("remove_link_from_post/", views.BackOnly.remove_link_from_post, name="remove_link_from_post"),
    path("add_link_to_post/", views.BackOnly.add_link_to_post, name="add_link_to_post"),
    path("get_available_links/", views.BackOnly.get_available_links, name="get_available_links"),
]