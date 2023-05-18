from django.contrib import admin

from .models import Reply, Reaction, Tweet, ReactionType, TweetImages, ReplyReaction


@admin.display(description='Short text')
def get_short_text(obj):
    return f'{obj.text[:20]}...'


class TweetImagesInline(admin.TabularInline):
    model = TweetImages
    extra = 1


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    inlines = [
        TweetImagesInline,
    ]
    date_hierarchy = 'created_at'
    actions_on_bottom = True
    actions_on_top = False
    empty_value_display = '--empty--'
    # exclude = ['profile', 'image']
    # fields = ['text', ]
    fields = (('text', 'profile'), 'image')
    list_display = ['id',
                    'get_profile_fullname',
                    get_short_text,
                    'get_reactions_str',
                    'image',
                    'created_at'
                    ]
    list_display_links = [get_short_text, 'id']
    list_editable = ['image', ]
    list_filter = ['created_at', 'profile']
    list_per_page = 2
    save_as = True
    search_fields = ['text', "profile__user__username__exact"]
    sortable_by = ['created_at', 'id']

    def get_profile_fullname(self, obj):
        return obj.profile.user.get_full_name()


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    actions_on_top = False
    actions_on_bottom = True
    empty_value_display = '-'
    fields = (('profile', 'text'), 'tweet')
    list_display = [
        'id',
        'profile',
        'get_fullname',
        get_short_text,
        'get_reactions',
        'created_at',
        'tweet'
    ]
    list_display_links = [get_short_text, ]
    list_editable = ['profile', ]
    search_fields = ['text', 'profile__user__username__exact']
    sortable_by = ['created_at', 'id']

    def get_fullname(self, obj):
        return obj.profile.user.get_full_name()


@admin.register(ReplyReaction)
class ReplyReactionAdmin(admin.ModelAdmin):
    pass


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    pass


@admin.register(ReactionType)
class ReactionTypeAdmin(admin.ModelAdmin):
    pass
