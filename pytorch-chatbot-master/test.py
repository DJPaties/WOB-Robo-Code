import requests

pic_url = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-4vMXsWROfhpNK0i67MhkbVan/user-fIGzMafApcfr5YeTOphjWDKR/img-inEHIDR17xhq5pBcT7zIuA9h.png?st=2024-01-15T12%3A42%3A38Z&se=2024-01-15T14%3A42%3A38Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-01-15T05%3A45%3A48Z&ske=2024-01-16T05%3A45%3A48Z&sks=b&skv=2021-08-06&sig=DZpzaNGDvSH9vi8vh4rtD3%2BOFyATPrnXrAW%2BdSdIhuY%3D"

with open('pic1.jpg', 'wb') as handle:
    response = requests.get(pic_url, stream=True)

    if not response.ok:
        print(response)

    for block in response.iter_content(1024):
        if not block:
            break

        handle.write(block)