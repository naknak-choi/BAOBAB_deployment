from allauth.account.adapter import DefaultAccountAdapter

class UserAdapter(DefaultAccountAdapter):
    
    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, False)
        data = form.cleaned_data
        
        nickname = data.get('nickname')
        
        if nickname:
            user.nickname = nickname
            
        user.save()
        
        return user