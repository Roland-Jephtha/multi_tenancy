from django.shortcuts import redirect
from django.conf import settings

class OnboardingMiddleware:
    """
    Redirects users to onboarding if their 'position' field is empty or None.
    Allows access to onboarding and logout URLs.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            onboarding_url = settings.ONBOARDING_REDIRECT_URL
            allowed_paths = [
                onboarding_url,
                '/logout/',  # adjust if your logout URL is different
            ]
            # Allow access to onboarding and logout URLs
            if not getattr(request.user, 'position', None):
                if not any(request.path.startswith(path) for path in allowed_paths):
                    return redirect(onboarding_url)
        return self.get_response(request)