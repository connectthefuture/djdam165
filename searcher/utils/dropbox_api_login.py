import dropbox

__author__ = 'johnb'

# Get your app key and secret from the Dropbox developer website
app_key = 'ikcr68gddbxed1t'
app_secret = 'i4wjfxe0umdvx7c'

private_access_token = 'aFNqVSoDKPEAAAAAAAAMR4wMdhoO3Cs0D6BUjX82-bE7Q689jokjSxLDyvujUEpJ'


def main():
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

    authorize_url = flow.start()
    # print '1. Go to: ' + authorize_url
    # print '2. Click "Allow" (you might have to log in first)'
    # print '3. Copy the authorization code.'
    # code = raw_input("Enter the authorization code here: ").strip()

    # This will fail if the user enters an invalid authorization code
    if private_access_token:
        access_token = private_access_token
    else:
        access_token, user_id = flow.finish(raw_input("Enter the authorization code here: ").strip())

    client = dropbox.client.DropboxClient(access_token)
    print 'linked account: ', client.account_info()
    return client

if __name__ == '__main__':
    main()

## Upload File from pwd to Dropbox
# f = open('crontab.txt', 'rb')
# response = client.put_file('/crontab.txt', f)
# print 'uploaded: ', response
#
#
# ## Downloadfile from Dropbox to pwd
# folder_metadata = client.metadata('/')
# print 'metadata: ', folder_metadata
#
# f, metadata = client.get_file_and_metadata('/crontab.txt')
# out = open('crontab.txt', 'wb')
# out.write(f.read())
# out.close()
# print metadata

