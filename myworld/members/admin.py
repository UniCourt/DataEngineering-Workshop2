from django.contrib import admin, messages

from .models import Blog, Students


def run_scraper(modeladmin, request, queryset):
    try:
        from web_scrapper import start_extraction

        start_extraction()

        modeladmin.message_user(
            request,
            "Scraper completed successfully. Blog records have been refreshed.",
            messages.SUCCESS,
        )

    except Exception as exc:
        modeladmin.message_user(
            request,
            f"Scraper failed: {exc}",
            messages.ERROR,
        )


run_scraper.short_description = "Run scraper and refresh blog records"


class DjStudentAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "address",
        "roll_number",
        "mobile",
        "branch",
    )

    list_filter = ("branch",)


class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "release_date",
        "blog_time",
        "created_date",
    )

    list_filter = ("author",)
    actions = [run_scraper]


admin.site.register(Students, DjStudentAdmin)
admin.site.register(Blog, BlogAdmin)