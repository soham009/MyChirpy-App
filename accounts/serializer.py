from rest_framework import serializers
from accounts.models import Portal_User
import random
from accounts.send_sms import replaceSpaces

class UserSerializer(serializers.ModelSerializer):

    # password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = Portal_User
        fields= ['first_name', 'email','username','Mobile_No','password','Otp','user_role']

       
    def save(self):
        number = random.randint(1000,9999) 
        account = Portal_User(
            first_name=self.validated_data['first_name'],
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            Mobile_No=self.validated_data['Mobile_No'],
            user_role = 2,
            Otp = number
        )
        password=self.validated_data['password'],
        account.set_password(password)
        account.save()
        return account
