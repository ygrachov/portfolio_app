This is a sample application that might be used as a corporate/internet forum
It allows logged in users to start topic, add text information, upload pictures and comment topics. All users are allowed to read the information
All inputs are editable for an input owner
Superuser 'user1' with password '111' was created initially
Styles are not perfect and were added only for the app not being so ugly looking )
The app is written in Python 3.9 using Django framework and uses the standard Django classes
One may want to use a social login features which requires obtaining OAUTH2 credentials from GitHub(settings/developer settings) and Google (google cloud platform) and changing 4 lines in the settings.py (i.e.SOCIAL_AUTH_GITHUB_KEY, SOCIAL_AUTH_GITHUB_SECRET, SOCIAL_AUTH_GOOGLE_OAUTH2_KEY, SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET). Initial credentials are removed from sample for security reason.
