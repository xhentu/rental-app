import random
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
# ⚠️ သင့် App အမည်ကို အောက်မှာ သေချာပြောင်းပေးပါ
from listings.models import Listing  

User = get_user_model()

# 👤 ၁။ လက်ရှိ DB ထဲမှာရှိပြီးသား User တွေကို ဆွဲထုတ်ခြင်း
all_users = list(User.objects.all())

if not all_users:
    raise Exception("🚨 Database ထဲမှာ User တစ်ယောက်မှ မရှိသေးပါဘူး! အရင်ဆုံး App ကနေ User အနည်းဆုံး တစ်ယောက် ဆောက်ပေးပါဗျာ။")

# ရှိသမျှ User တွေထဲကမှ အယောက် ၅ ယောက် (သို့မဟုတ် ရှိသမျှအကုန်) ကို Random ရွေးထုတ်ခြင်း
sample_size = min(len(all_users), 5)
fake_landlords = random.sample(all_users, sample_size)

regions = ['ရန်ကုန်တိုင်းဒေသကြီး', 'မန္တလေးတိုင်းဒေသကြီး', 'နေပြည်တော်', 'ပဲခူးတိုင်းဒေသကြီး', 'ရှမ်းပြည်နယ်']
townships = {
    'ရန်ကုန်တိုင်းဒေသကြီး': ['လှိုင်', 'ကမာရွတ်', 'ဗဟန်း', 'စမ်းချောင်း', 'ရန်ကင်း', 'မရမ်းကုန်း', 'တာမွေ', 'တောင်ဥက္ကလာပ'],
    'မန္တလေးတိုင်းဒေသကြီး': ['ချမ်းအေးသာစံ', 'မဟာအောင်မြေ', 'ပြည်ကြီးတံခွန်', 'ချမ်းမြသာစံ', 'အောင်မြေသာစံ'],
    'နေပြည်တော်': ['ဇမ္ဗူသီရိ', 'ဒက္ခိဏသီရိ', 'ပုဗ္ဗသီရိ', 'ဥတ္တရသီရိ'],
    'ပဲခူးတိုင်းဒေသကြီး': ['ပဲခူးမြို့', 'တောင်ငူမြို့', 'ပြည်မြို့'],
    'ရှမ်းပြည်နယ်': ['တောင်ကြီးမြို့', 'လားရှိုးမြို့', 'ကလောမြို့']
}
quarters = ['၁ ရပ်ကွက်', '၂ ရပ်ကွက်', '၃ ရပ်ကွက်', '၄ ရပ်ကွက်', 'အောင်မြေသာစံ ရပ်ကွက်', 'ရွှေပြည်သာ ရပ်ကွက်', 'မြေနီကုန်း ရပ်ကွက်']
roads = ['ပြည်လမ်း', 'ကမ္ဘာအေးဘုရားလမ်း', 'အင်းစိန်လမ်း', 'မဟာဗန္ဓုလလမ်း', 'ဗိုလ်ချုပ်လမ်း', 'ဓမ္မစေတီလမ်း']

# သင့် မော်ဒယ်ထဲက CATEGORY_CHOICES အတိုင်း ကွက်တိ ပြောင်းလဲထားခြင်း
property_types = ['house', 'condo', 'apartment', 'shop', 'office', 'hostel', 'industrial', 'warehouse', 'land']
offer_types = ['sale', 'rent', 'buy', 'tenant']
facings = ['အရှေ့', 'အနောက်', 'တောင်', 'မြောက်', 'အရှေ့တောင်', 'အရှေ့မြောက်']

# Remarks & Land pools
generic_remarks = [
    "နေရာကောင်း စျေးနှုန်းတန်သည်။ ရေမီးအစုံပါဝင်ပြီး အသင့်နေရုံ ပြင်ဆင်ပေးထားသည်။ လူစည်ကားသော ပတ်ဝန်းကျင်ဖြစ်သည်။",
    "အမြန်ငှားမည်/ရောင်းမည်။ ပိုင်ရှင်တိုက်ရိုက်ဖြစ်၍ အရှုပ်အရှင်းကင်းကြောင်း ရာနှုန်းပြည့် အာမခံပါသည်။"
]
landmarks_pool = ['City Mart အနီး', 'ဈေးနီး', 'ကားမှတ်တိုင်နီး', 'ကျောင်းနီး', 'Main Road အနီး']
land_types_pool = ['ဘိုးဘွားပိုင်မြေ', 'ဂရန်မြေ', 'ပါမစ်မြေ', 'လယ်ယာမြေ ပြောင်းလဲပြီး']

print(f"⏳ Seeding 130 listings matching your exact models.py across {len(fake_landlords)} users...")

for i in range(130):
    region = random.choice(regions)
    township = random.choice(townships[region])
    property_type = random.choice(property_types)
    offer_type = random.choice(offer_types)
    chosen_landlord = random.choice(fake_landlords)

    # 💰 စျေးနှုန်း သတ်မှတ်ချက်
    if offer_type in ['sale', 'buy']:
        price = random.choice([450, 680, 850, 1200, 2500, 4500, 6000, 9800, 15000])
    else:
        price = random.choice([2.5, 3.5, 5, 8, 12, 15, 25, 40]) * 100000

    # 📐 သင့်မော်ဒယ်ရှိ DecimalField ပုံစံအတိုင်း ရေးသွင်းခြင်း
    width = float(random.choice([15, 20, 25, 40, 50]))
    length = float(random.choice([40, 50, 60, 70, 80]))
    road = random.choice(roads)
    quarter = random.choice(quarters)
    title = f"{township}မြို့နယ်ရှိ အိမ်ခြံမြေ အမြန်ကိစ္စ (#I-{i+1})"

    # Hostel နှင့် Land တို့အတွက် သီးသန့် field များကို ကိုင်တွယ်ခြင်း
    hostel_type = random.choice(['Male', 'Female', 'Both', 'Family']) if property_type == 'hostel' else None
    type_of_land = random.choice(land_types_pool) if property_type == 'land' else None

    Listing.objects.create(
        landlord=chosen_landlord,
        offer_type=offer_type,
        property_type=property_type,
        region=region,
        township=township,
        quarter=quarter,
        road=road,
        landmarks=random.sample(landmarks_pool, random.randint(1, 3)),
        
        # Latitude & Longitude (Optional)
        latitude=None,
        longitude=None,
        
        width=width,
        length=length,
        # area_dimension_text ကို သင့် save() က auto တွက်မှာမို့ ထည့်စရာမလိုပါ
        
        floor_data={
            'type': random.choice(['ground', 'normal', 'top']),
            'level': random.randint(1, 8)
        },
        room_structure={
            'master_bed': random.randint(0, 2),
            'single_bed': random.randint(1, 3),
            'bathroom': random.randint(1, 2)
        },
        features={
            'facing': random.choice(facings),
            'fully_repaired': random.choice([True, False])
        },
        
        title=title,
        remark=random.choice(generic_remarks)[:200], # max_length=200 ကာကွယ်ရန်
        price=price,
        hostel_type=hostel_type,
        type_of_land=type_of_land,
        
        owner_direct=random.choice([True, False]),
        price_negotiable=random.choice([True, False]),
        installment_available=random.choice([True, False]),
        bank_transfer_accepted=random.choice([True, False]),
        is_presale=random.choice([True, False]),
        
        payment_details={},
        active_buttons={'call': True, 'viber': random.choice([True, False])},
        contact_phone=f"09{random.randint(200000000, 999999999)}",
        contact_phone1=f"09{random.randint(200000000, 999999999)}" if random.choice([True, False]) else None,
        contact_phone2=None,
        viber_contact=None,
        telegram_username=None,
        whatsapp_number=None,
        
        is_active=True,
        is_boosted=random.choice([True, False]),
        is_premium=random.choice([True, False]),
        is_completed=False,
        is_deleted=False,
        
        # 💡 DB Level NOT NULL Integrity Error ကို ကျော်လွှားရန် စတင်သတ်မှတ်ပေးခြင်း
        expiry_date=timezone.now() + timedelta(days=90) 
    )

print("🎉 Done! Your database is now seeded perfectly according to your original model structures.")