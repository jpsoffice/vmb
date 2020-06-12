from vmb.matrimony.models import Occupation, OccupationCategory, Education, EducationCategory

with open("rw.txt") as fo:
    k=0
    for i in fo:
        k += 1
        if k<=8:
            obj = Occupation(name=i, category=OccupationCategory.objects.filter(name__contains="Administration")[0])
            obj.pk = k-1
            obj.save()
        elif k>8 and k<=10:
            obj = Occupation(name=i, category=OccupationCategory.objects.filter(name__contains="Agriculture")[0])
            obj.pk = k-1
            obj.save()
        elif k>10 and k<=13:
            obj = Occupation(name=i, category=OccupationCategory.objects.filter(name__contains="Airline")[0])
            obj.pk = k-1
            obj.save()
        elif k>13 and k<=15:
            obj = Occupation(name=i, category=OccupationCategory.objects.filter(name__contains="Architecture & design")[0])
            obj.pk = k-1
            obj.save()
        elif k>15 and k<=23:
            obj = Occupation(name=i, category=OccupationCategory.objects.filter(name__contains="Banking & finance")[0])
            obj.pk = k-1
            obj.save()
        elif k>23 and k<=29:
            obj = Occupation(name=i, category=OccupationCategory.objects.filter(name__contains="Beauty & fashion")[0])
            obj.pk = k-1
            obj.save()
        elif k>29 and k<=31:
            obj = Occupation(name=i, category=OccupationCategory.objects.filter(name__contains="Bpo & customer service")[0])
            obj.pk = k-1
            obj.save()
        elif k>31 and k<=32:
            obj = Occupation(name=i, category=OccupationCategory.objects.filter(name__contains="Civil services")[0])
            obj.pk = k-1
            obj.save()
        elif k>32 and k<=43:
            obj = Occupation(name=i, category=OccupationCategory.objects.filter(name__contains="Corporate professionals")[0])
            obj.pk = k-1
            obj.save()
        elif k>43 and k<=48:
            obj = Occupation(name=i, category=OccupationCategory.objects.filter(name__contains="Defence")[0])
            obj.pk = k-1
            obj.save()
        elif k>48 and k<=54:
            obj = Occupation(name=i, category=OccupationCategory.objects.filter(name__contains="Education & training")[0])
            obj.pk = k-1
            obj.save()
        elif k>54 and k<=62:
            obj = Occupation(name=i, category=OccupationCategory.objects.filter(name__contains="Engineering")[0])
            obj.pk = k-1
            obj.save()
        elif k>62 and k<=65:
            obj = Occupation(name=i, category=OccupationCategory.objects.filter(name__contains="Hospitality")[0])
            obj.pk = k-1
            obj.save()
        elif k>65 and k<=79:
            obj = Occupation(name=i, category=OccupationCategory.objects.filter(name__contains="It & software")[0])
            obj.pk = k-1
            obj.save()
        elif k>79 and k<=81:
            obj = Occupation(name=i, category=OccupationCategory.objects.filter(name__contains="Legal")[0])
            obj.pk = k-1
            obj.save()
        elif k>81 and k<=83:
            obj = Occupation(name=i, category=OccupationCategory.objects.filter(name__contains="Law enforcement")[0])
            obj.pk = k-1
            obj.save()
        elif k>83 and k<=97:
            obj = Occupation(name=i, category=OccupationCategory.objects.filter(name__contains="Medical & healthcare")[0])
            obj.pk = k-1
            obj.save()
        elif k>97 and k<=105:
            obj = Occupation(name=i, category=OccupationCategory.objects.filter(name__contains="Media & entertainment")[0])
            obj.pk = k-1
            obj.save()
        elif k>105 and k<=107:
            obj = Occupation(name=i, category=OccupationCategory.objects.filter(name__contains="Merchant navy")[0])
            obj.pk = k-1
            obj.save()
        elif k>107 and k<=108:
            obj = Occupation(name=i, category=OccupationCategory.objects.filter(name__contains="Scientist")[0])
            obj.pk = k-1
            obj.save()
        elif k>108 and k<=110:
            obj = Occupation(name=i, category=OccupationCategory.objects.filter(name__contains="Top management")[0])
            obj.pk = k-1
            obj.save()
        elif k>110 and k<=140:
            obj = Occupation(name=i, category=OccupationCategory.objects.filter(name__contains="Others")[0])
            obj.pk = k-1
            obj.save()
        else: 
            print("Done")

with open("rw.txt") as fo:
    k=0
    for i in fo:
        k += 1
        if k<=9:
            obj = Education(name=i, category=EducationCategory.objects.filter(name__contains="Any Bachelors in Engineering / Computers")[0])
            obj.pk = k-1
            obj.save()
        elif k>9 and k<=17:
            obj = Education(name=i, category=EducationCategory.objects.filter(name__contains="Any Masters in Engineering / Computers")[0])
            obj.pk = k-1
            obj.save()
        elif k>17 and k<=29:
            obj = Education(name=i, category=EducationCategory.objects.filter(name__contains="Any Bachelors in Arts / Science / Commerce")[0])
            obj.pk = k-1
            obj.save()
        elif k>29 and k<=38:
            obj = Education(name=i, category=EducationCategory.objects.filter(name__contains="Any Masters in Arts / Science / Commerce")[0])
            obj.pk = k-1
            obj.save()
        elif k>38 and k<=43:
            obj = Education(name=i, category=EducationCategory.objects.filter(name__contains="Any Bachelors in Management")[0])
            obj.pk = k-1
            obj.save()
        elif k>43 and k<=50:
            obj = Education(name=i, category=EducationCategory.objects.filter(name__contains="Any Masters in Management")[0])
            obj.pk = k-1
            obj.save()
        elif k>50 and k<=61:
            obj = Education(name=i, category=EducationCategory.objects.filter(name__contains="Any Bachelors in Medicine in General / Dental / Surgeon")[0])
            obj.pk = k-1
            obj.save()
        elif k>61 and k<=67:
            obj = Education(name=i, category=EducationCategory.objects.filter(name__contains="Any Masters in Medicine - General / Dental / Surgeon")[0])
            obj.pk = k-1
            obj.save()
        elif k>67 and k<=71:
            obj = Education(name=i, category=EducationCategory.objects.filter(name__contains="Any Bachelors in Legal")[0])
            obj.pk = k-1
            obj.save()
        elif k>71 and k<=74:
            obj = Education(name=i, category=EducationCategory.objects.filter(name__contains="Any Masters in Legal")[0])
            obj.pk = k-1
            obj.save()
        elif k>71 and k<=79:
            obj = Education(name=i, category=EducationCategory.objects.filter(name__contains="Any Financial Qualification - ICWAI / CA / CS/ CFA")[0])
            obj.pk = k-1
            obj.save()
        elif k>79 and k<=85:
            obj = Education(name=i, category=EducationCategory.objects.filter(name__contains="Service - IAS / IPS / IRS / IES / IFS")[0])
            obj.pk = k-1
            obj.save()
        elif k>85 and k<=86:
            obj = Education(name=i, category=EducationCategory.objects.filter(name__contains="Ph.D.")[0])
            obj.pk = k-1
            obj.save()
        elif k>86 and k<=90:
            obj = Education(name=i, category=EducationCategory.objects.filter(name__contains="Any Diploma")[0])
            obj.pk = k-1
            obj.save()
        elif k>90 and k<=91:
            obj = Education(name=i, category=EducationCategory.objects.filter(name__contains="Higher Secondary / Secondary")[0])
            obj.pk = k-1
            obj.save()
        else:
            print("Done")


>>> from datetime import date
>>> date.fromisoformat('2019-12-04')
datetime.date(2019, 12, 4)