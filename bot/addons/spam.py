import urllib2

import mandrillwrapper


# spam->http://pastebin.com/raw.php?i=qzCh8DCe-http://pastebin.com/raw.php?i=AAF54Du3
# http://pastebin.com/raw.php?i=PRm68quh
def spam(to_url, msg_url):
    # print to_url +" "+msg_url
    try:
        to_data = urllib2.urlopen(to_url)
        msg_data = urllib2.urlopen(msg_url)
        to_list = []
        msgs = ""
        for mail in to_data:
            to_list.append(mail)
        for txt in msg_data:
            if txt.find('FROM') != -1:
                fromadd = txt.split(":")[1]
            elif txt.find('SUBJECT') != -1:
                subj = txt.split(":")[1]
            elif txt.find('APIKEY') != -1:
                apikey = txt.split(":")[1]
            else:
                msgs += txt
    except:
        return "Failed to retrieve sources."
    try:
        post_mail(to_list, msgs, subj, fromadd, apikey)
        return "Send"
    except:
        return "Failed to send."


def post_mail(to_list, msgs, subj, fromadd, apikey):
    mandrill_client = mandrillwrapper.Mandrill(apikey.replace("\n", "").replace("\r", ""))
    message = {
        'from_email': fromadd,
        'from_name': fromadd.split("@")[0],
        'html': '<p>' + msgs + '</p>',
        'important': False,
        'merge': True,
        'subject': subj,
        'to': [{'email': ",".join(to_list)}]
    }
    mandrill_client.messages.send(message=message, async=False)
