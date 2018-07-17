from random import randint
from urllib import request, error


class Daily:
    """
    A Class to generate an AdFly-Link for a Dailylink to get some Items.
    getCode via MySql ->
    generates AdFly Link with startlink with start value to bot ->
    if was Activated False:
        "Start" Bot -> set was Code Activated -> True

    api.adf.ly/api.php?
    key=35b879ad2475c660b8618839997596db
    uid=18563429&advert_type=banner&domain=adf.ly&url=https://www.google.de

    After 0:00 set WasCodeActivated to False on every User
    """
    def __init__(self, _public_key, _user_id):
        """
        Sets LogIn-Values
        :param _public_key: String - User Key
        :param _user_id: String - User ID
        """
        self.public_key = _public_key
        self.user_id = _user_id

    def generate_link(self, url, ad_type = "int"):
        """
        generates an adf.ly link
        :param url: Url to convert
        :param ad_type: the ad-type "banner" or "int" redirected Link
        :return: new adf.ly link as string
        """
        apiurl = ""
        apiurl += "http://api.adf.ly/api.php?key=" + self.public_key + \
                  "&uid=" + self.user_id + \
                  "&advert_type=" + ad_type +\
                  "&url=" + url
        res = ""
        try:
            s = request.urlopen(url)
            res = s.read()
        except error.URLError:  # as e:
            pass
            # TODO Handle URLError
        return res

    @classmethod
    def generate_code(cls):
        """
        Generates new code in database
        """
        result = ""
        for i in range(0, 7):
            result += str(randint(0, 9))
        # d = get_database()

        # TODO Generate Code

    @classmethod
    def reset_all_user(cls):
        """
        Resets all users' WasCodeActivated in MySQL to False
        """
        # TODO Reset all Code entries for all users
        return 0
