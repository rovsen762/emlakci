# from django.db import models

# from utils.photo_save import logo_dir_path
# from django.core.validators import FileExtensionValidator


# class MainData(models.Model):
#     header_logo = models.ImageField(upload_to=logo_dir_path,verbose_name='Loqonun header hissədəki şəkli')
#     favicon = models.ImageField(upload_to=logo_dir_path,verbose_name='Favikon şəkli')
#     footer_logo = models.ImageField(upload_to=logo_dir_path,verbose_name='Loqonun footer hissədəki şəkli')
#     banner_image = models.ImageField(upload_to=logo_dir_path,null=True,blank=True,verbose_name="Ana səhifə şəkli")
#     banner_text = models.CharField(max_length=300,blank=True,null=True, verbose_name="Ana səhifə mətni")
#     banner_subtext = models.CharField(max_length=300,blank=True,null=True, verbose_name="Ana səhifə alt mətni")
#     phone = models.CharField(max_length=100,blank=True,null=True, verbose_name="Əsas telefon nömrəsi")
#     email = models.EmailField(max_length=100,blank=True,null=True, verbose_name="Əsas mail")
#     address = models.TextField(verbose_name="Ünvan") 
#     created_at = models.DateTimeField(auto_now_add=True,verbose_name="Yaradılma tarixi")
#     updated_at = models.DateTimeField(auto_now=True,verbose_name="Yenilənmə tarixi")
#     def __str__(self):
#         return "Saytın Statik Məlumatları"
    
#     class Meta:
#         verbose_name = _('Saytın statik məlumatları')
#         verbose_name_plural = _('Saytın Statik Məlumatları')



# class BannerImages(models.Model):
#     maindata = models.ForeignKey(MainData, on_delete=models.CASCADE, related_name='banner_images')
#     name = models.CharField(max_length=100,verbose_name=_("Adı"))
#     image = models.ImageField(upload_to=logo_dir_path,null=True,blank=True,verbose_name=_("Banner şəkli"))
#     created_at = models.DateTimeField(auto_now_add=True,verbose_name="Yaradılma tarixi")
#     updated_at = models.DateTimeField(auto_now=True,verbose_name="Yenilənmə tarixi")
#     def __str__(self):
#         return self.name
    
    
#     class Meta:
#         ordering = ['-created_at']
#         verbose_name = _('Banner Şəkli')
#         verbose_name_plural = _('Banner Şəkilləri')
    

  
# class SocMedia(models.Model):
#     name = models.CharField(max_length=100,verbose_name=_("Adı"))
#     icon = models.ImageField(upload_to=logo_dir_path,verbose_name=_("Şəbəkənin loqosu"), blank=True, null=True)
#     link = models.URLField(max_length = 200,verbose_name=_("Link"))
#     created_at = models.DateTimeField(auto_now_add=True,verbose_name="Yaradılma tarixi")
#     updated_at = models.DateTimeField(auto_now=True,verbose_name="Yenilənmə tarixi")

#     def __str__(self):
#         return self.name    
    
#     class Meta:
#         ordering = ['-created_at']
#         verbose_name = "Sosial Media Hesabı"
#         verbose_name_plural = "Sosial Media Hesabları"


# class About(models.Model):
#     title = models.CharField(verbose_name=_("Başlıq"),max_length=255)
#     description = models.TextField  (verbose_name=_("Açıqlama"))
#     created_at = models.DateTimeField(auto_now_add=True,verbose_name="Yaradılma tarixi")
#     updated_at = models.DateTimeField(auto_now=True,verbose_name="Yenilənmə tarixi")

#     def __str__(self):
#         return self.title
    
#     class Meta:
#         ordering = ['-created_at']
#         verbose_name = _("Haqqımızda")
#         verbose_name_plural = _("Haqqımızda")


# class Team(models.Model):
#     first_name = models.CharField(verbose_name=_("Adı"),max_length=255)
#     last_name = models.CharField(verbose_name=_("Soyadı"),max_length=255)    
#     image = models.ImageField(upload_to=logo_dir_path,verbose_name=_("Şəkil"))
#     position = models.CharField(verbose_name=_("Vəzifə"),max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True,verbose_name="Yaradılma tarixi")
#     updated_at = models.DateTimeField(auto_now=True,verbose_name="Yenilənmə tarixi")
    

#     def __str__(self):
#         return self.first_name
    
#     class Meta:
#         verbose_name = _("Komanda")
#         verbose_name_plural = _("Komanda")
        


# class TeamSocMedia(models.Model):
#     team_member = models.ForeignKey(Team, on_delete=models.CASCADE,verbose_name=_("Komanda üzvü"), related_name="team_socmedias")
#     name = models.CharField(max_length=100,verbose_name=_("Adı"))
#     icon = models.ImageField(upload_to=logo_dir_path,verbose_name=_("Şəbəkənin loqosu"), blank=True, null=True)
#     link = models.URLField(max_length = 400,verbose_name=_("Link"))
#     created_at = models.DateTimeField(auto_now_add=True,verbose_name="Yaradılma tarixi")
#     updated_at = models.DateTimeField(auto_now=True,verbose_name="Yenilənmə tarixi")

#     def __str__(self):
#         return self.name    
    
#     class Meta:
#         verbose_name = _("Komanda Üzvünün Sosial Media Hesabı")
#         verbose_name_plural = _("Komanda Üzvlərinin Sosial Media Hesabları")
    
    
# class TermsCondition(models.Model):
#     title = models.CharField(verbose_name=_("Başlıq"),max_length=255)
#     description = RichTextField(verbose_name=_("Açıqlama"),)
#     created_at = models.DateTimeField(auto_now_add=True,verbose_name="Yaradılma tarixi")
#     updated_at = models.DateTimeField(auto_now=True,verbose_name="Yenilənmə tarixi")

#     def __str__(self):
#         return self.title

#     class Meta:
#         ordering = ['-created_at']
#         verbose_name = _("İstifadəçi razılaşması məlumatı")
#         verbose_name_plural = _("İstifadəçi razılaşması məlumatları")

        
# class ReturnPolicy(models.Model):
#     title = models.CharField(verbose_name=_("Başlıq"),max_length=255)
#     description = RichTextField(verbose_name=_("Açıqlama"),)
#     created_at = models.DateTimeField(auto_now_add=True,verbose_name="Yaradılma tarixi")
#     updated_at = models.DateTimeField(auto_now=True,verbose_name="Yenilənmə tarixi")

#     def __str__(self):
#         return self.title

#     class Meta:
#         ordering = ['-created_at']
#         verbose_name = _("Məhsulun geri qaytarılma şərti")
#         verbose_name_plural = _("Məhsulun geri qaytarılma şərtləri")


# class Faq(models.Model):
#     question = models.CharField(verbose_name=_("Sual"),max_length=300)
#     answer = RichTextField( verbose_name=_("Cavab"),)
#     created_at = models.DateTimeField(auto_now_add=True,verbose_name="Yaradılma tarixi")
#     updated_at = models.DateTimeField(auto_now=True,verbose_name="Yenilənmə tarixi")

#     def __str__(self):
#         return self.question

#     class Meta:
#         ordering = ['-created_at']
#         verbose_name = _("F.A.Q")
#         verbose_name_plural = _("F.A.Q")


# class Contact(models.Model):
#     name = models.CharField(max_length=100,verbose_name=_("Adı"))
#     phone = models.CharField(max_length=100,verbose_name=_("Telefon"))
#     subject = models.CharField(max_length=200,verbose_name=_("Mövzu"))
#     message = models.TextField(verbose_name=_("Mesaj"))
#     date = models.DateTimeField(auto_now_add=True,verbose_name="Yaradılma tarixi")

#     def __str__(self):
#         return self.name


#     class Meta:
#         verbose_name = "Əlaqələr"
#         verbose_name_plural = "Əlaqələr"


# class Phone(models.Model):
#     maindata = models.ForeignKey(MainData, default=None, on_delete=models.CASCADE, related_name='phones')
#     phone = models.CharField(max_length=100,blank=True,null=True)

#     def __str__(self):
#         return self.phone
    
#     class Meta:
#         verbose_name = "Telefonlar"
#         verbose_name_plural = "Telefonlar"
    



# class Email(models.Model):
#     maindata = models.ForeignKey(MainData, default=None, on_delete=models.CASCADE, related_name='emails')
#     email = models.EmailField(max_length=100,blank=True,null=True)

#     def __str__(self):
#         return self.email or "No email provided"
    
#     class Meta:
#         verbose_name = "Emaillər"
#         verbose_name_plural = "Emaillər"


# class Address(models.Model):
#     maindata = models.ForeignKey(MainData, default=None, on_delete=models.CASCADE, related_name='addresses')
#     address = models.CharField(max_length=400)

#     def __str__(self):
#         return self.address
    
#     class Meta:
#         verbose_name = "Addresslər"
#         verbose_name_plural = "Addresslər"


# class Subscription(models.Model):
#     subemail = models.EmailField(max_length=100,blank=True,null=True)
#     updated_at = models.DateTimeField(auto_now=True,verbose_name="Yenilənmə tarixi")
#     created_at = models.DateTimeField(auto_now_add=True,verbose_name="Yaradılma tarixi")    

#     def __str__(self):
#         return self.subemail or "No email provided"
    
#     class Meta:
#         ordering = ['-created_at']
#         verbose_name = "Abunələr"
#         verbose_name_plural = "Abunələr"



# class Seo(models.Model):
#     author = models.CharField(max_length=100, null=True, blank=True)

#     class Meta:
#         verbose_name = "SEO"
#         verbose_name_plural = "SEO"

#     def __str__(self) :
#         return "SEO"

# class SeoKeywords(models.Model):
#     seo = models.ForeignKey(Seo, related_name="keywords", null=True, blank=True, on_delete=models.CASCADE)
#     keywords = models.CharField(max_length=200, null=True, blank=True)
#     class Meta:
#         verbose_name = "Keywords"
#         verbose_name_plural = "Keywords"

# class SeoDescription(models.Model):
#     seo = models.ForeignKey(Seo, related_name="description", null=True, blank=True, on_delete=models.CASCADE)
#     description = models.CharField(max_length=200, null=True, blank=True)
#     class Meta:
#         verbose_name = "Description"
#         verbose_name_plural = "Description"