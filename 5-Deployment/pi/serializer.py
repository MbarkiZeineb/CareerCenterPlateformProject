from rest_framework import serializers
from .models import profilfinal, profilreco, jobofferfinal, userrecommandation, jobseekerfinal, coursfinal

class profilfinalSerializer(serializers.ModelSerializer):

    class Meta:
        model = profilfinal
        fields = '__all__'

class profilrecoSerializer(serializers.ModelSerializer):

    class Meta:
        model = profilreco
        fields = '__all__'

class jobseekerfinalSerializer(serializers.ModelSerializer):

    class Meta:
        model = jobseekerfinal
        fields = '__all__'

class jobofferfinalSerializer(serializers.ModelSerializer):

    class Meta:
        model = jobofferfinal
        fields = '__all__'

class userrecommandationSerializer(serializers.ModelSerializer):

    class Meta:
        model = userrecommandation
        fields = '__all__'

class coursfinalSerializer(serializers.ModelSerializer):

    class Meta:
        model = coursfinal
        fields = '__all__'
        