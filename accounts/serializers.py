# serializers.py
from rest_framework import serializers
import phonenumbers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'phone', 'country_code', 'is_whatsapp']
    
    def validate(self, attrs):
        phone = attrs.get('phone')
        country_code = attrs.get('country_code')
        
        # Check if phone is already in E164 format (starts with +)
        if phone and phone.startswith('+'):
            try:
                parsed = phonenumbers.parse(phone, None)
                if phonenumbers.is_valid_number(parsed):
                    # Phone is already formatted, just ensure country_code matches
                    attrs['phone'] = phone
                    attrs['country_code'] = f"+{parsed.country_code}"
                    return attrs
            except phonenumbers.NumberParseException:
                pass
        
        # Original validation logic for non-formatted numbers
        if not phone or not country_code:
            raise serializers.ValidationError("Phone and country code are required.")
        
        # Combine the country code and phone
        full_phone = f"{country_code}{phone}"
        try:
            parsed = phonenumbers.parse(full_phone, None)
        except phonenumbers.NumberParseException as e:
            raise serializers.ValidationError(f"Phone number could not be parsed: {e}")
        
        if not phonenumbers.is_valid_number(parsed):
            raise serializers.ValidationError("Phone number is invalid.")
        
        # Replace the plain phone with the formatted international version
        attrs['phone'] = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        attrs['country_code'] = f"+{parsed.country_code}"
        
        return attrs




class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'full_name', 'phone_number', 'address', 'role', 'profile_picture', 'category',
            'designation', 'about', 'enable_destination_and_company_name', 'business_name',
            'company_name', 'logo'
        ]

    def validate(self, attrs):
        role = attrs.get('role', None)

        if role == 'business':
            if not attrs.get('business_name'):
                raise serializers.ValidationError({"business_name": "This field is required for business role."})
            if not attrs.get('logo'):
                raise serializers.ValidationError({"logo": "This field is required for business role."})

        return attrs
