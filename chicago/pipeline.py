from requests import request, HTTPError

from django.core.files.base import ContentFile
from authenticate.models import Profile


def save_profile_picture(backend, user, response, *args, **kwargs):
	
	profile = Profile.objects.filter(user = user)

	if not profile.exists():

		profile = Profile.objects.create(user = user)

		if backend.name == 'facebook':
			profile.facebook = '{0}{1}'.format('https://facebook.com/', response['id'])
			profile.save()
			url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
			
			try:
				response = request('GET', url, params={'type': 'large'})
				response.raise_for_status()
				profile.profile_picture.save(
					'{0}_social.jpg'.format(user.username),
					ContentFile(response.content)
					)
				profile.save()
			except HTTPError:
				pass

		if backend.name == 'twitter':
			url = response.get('profile_image_url', '').replace('_normal','')
			profile.twitter = '{0}{1}'.format('https://twitter.com/', response['screen_name'])
			profile.save()
			try:
				response = request('GET', url, params={'type': 'large'})
				response.raise_for_status()
				profile.profile_picture.save(
					'{0}_twitter.jpg'.format(user.username),
					ContentFile(response.content)
					)
				profile.save()
			except HTTPError:
				pass

		if backend.name == 'google-oauth2':
			url = response['image'].get('url')
			profile.google = response['url']
			profile.save()
			try:
				response = request('GET', url, params={'sz': '200'})
				response.raise_for_status()
				profile.profile_picture.save(
					'{0}_google.jpg'.format(user.username),
					ContentFile(response.content)
					)
				profile.save()
			except HTTPError:
				pass