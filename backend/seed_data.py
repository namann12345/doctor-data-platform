"""
Seed data for Doctor Data Platform
Run: python seed_data.py (from backend/ directory)

Demo Accounts:
  User:  user@demo.com  / Demo@1234  (150 credits)
  Admin: admin@demo.com / Admin@1234 (500 credits)
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, create_tables
from app.models.user import User
from app.models.doctor import Doctor
from app.models.credit_package import CreditPackage
from app.utils.security import hash_password


def seed():
    create_tables()
    db = SessionLocal()

    try:
        print("Clearing existing seed data...")
        db.query(User).delete()
        db.query(Doctor).delete()
        db.query(CreditPackage).delete()
        db.commit()

        # ── Demo Users ──────────────────────────────────────────────
        print("Creating demo users...")
        user = User(
            email="user@demo.com",
            hashed_password=hash_password("Demo@1234"),
            full_name="Priya Sharma",
            phone="+91-9876543210",
            credit_balance=150,
            is_active=True,
            is_admin=False,
        )
        admin = User(
            email="admin@demo.com",
            hashed_password=hash_password("Admin@1234"),
            full_name="Rajesh Kumar",
            phone="+91-9876543211",
            credit_balance=500,
            is_active=True,
            is_admin=True,
        )
        db.add_all([user, admin])
        db.commit()
        print(f"  ✓ user@demo.com (ID: {user.id}, 150 credits)")
        print(f"  ✓ admin@demo.com (ID: {admin.id}, 500 credits, admin)")

        # ── Credit Packages ─────────────────────────────────────────
        print("Creating credit packages...")
        packages = [
            CreditPackage(
                name="Starter",
                description="Perfect for occasional searches",
                credits=100,
                bonus_credits=0,
                price=99.0,
                is_active=True,
                is_featured=False,
            ),
            CreditPackage(
                name="Growth",
                description="Most popular – best value for regular users",
                credits=500,
                bonus_credits=50,
                price=399.0,
                is_active=True,
                is_featured=True,
            ),
            CreditPackage(
                name="Professional",
                description="For healthcare researchers and professionals",
                credits=1000,
                bonus_credits=150,
                price=699.0,
                is_active=True,
                is_featured=False,
            ),
            CreditPackage(
                name="Enterprise",
                description="High-volume access for organizations",
                credits=2500,
                bonus_credits=500,
                price=1499.0,
                is_active=True,
                is_featured=False,
            ),
        ]
        db.add_all(packages)
        db.commit()
        for p in packages:
            print(f"  ✓ {p.name}: {p.credits}+{p.bonus_credits} credits @ ₹{p.price}")

        # ── Fictional Doctor Data ────────────────────────────────────
        print("Creating 30 fictional doctors...")

        doctors_data = [
            # Cardiology
            {
                "name": "Dr. Arjun Mehta",
                "specialty": "Cardiology",
                "qualification": "MD, DM Cardiology – AIIMS Delhi",
                "experience_years": 18,
                "hospital": "Apollo Hospitals",
                "city": "Mumbai",
                "state": "Maharashtra",
                "phone": "+91-22-4000-1001",
                "email": "arjun.mehta@apollodemo.in",
                "consultation_fee": 1200.0,
                "rating": 4.8,
                "total_reviews": 342,
                "bio": "Dr. Arjun Mehta is a senior interventional cardiologist with 18 years of expertise in complex angioplasties and cardiac rehabilitation. He completed his DM from AIIMS Delhi and has performed over 3,000 successful cardiac procedures. His research on minimally invasive cardiac interventions has been published in leading international journals.",
            },
            {
                "name": "Dr. Sunita Rao",
                "specialty": "Cardiology",
                "qualification": "MBBS, MD, DM – Cardiology, PGIMER Chandigarh",
                "experience_years": 12,
                "hospital": "Fortis Healthcare",
                "city": "Delhi",
                "state": "Delhi",
                "phone": "+91-11-4055-2002",
                "email": "sunita.rao@fortisdemo.in",
                "consultation_fee": 1000.0,
                "rating": 4.7,
                "total_reviews": 215,
                "bio": "Dr. Sunita Rao specializes in preventive cardiology and women's heart health. She trained at PGIMER Chandigarh and has been a pioneer in cardiac risk assessment programs in North India.",
            },
            # Neurology
            {
                "name": "Dr. Vikram Nair",
                "specialty": "Neurology",
                "qualification": "MBBS, MD, DM Neurology – NIMHANS Bangalore",
                "experience_years": 15,
                "hospital": "Manipal Hospital",
                "city": "Bangalore",
                "state": "Karnataka",
                "phone": "+91-80-2502-3003",
                "email": "vikram.nair@manipaldemo.in",
                "consultation_fee": 1100.0,
                "rating": 4.9,
                "total_reviews": 289,
                "bio": "Dr. Vikram Nair is a renowned neurologist specializing in epilepsy management and movement disorders. He completed his DM from NIMHANS and has treated over 5,000 patients with complex neurological conditions.",
            },
            {
                "name": "Dr. Preethi Krishnan",
                "specialty": "Neurology",
                "qualification": "MBBS, MD, DM – JIPMER Puducherry",
                "experience_years": 10,
                "hospital": "Apollo Hospitals",
                "city": "Chennai",
                "state": "Tamil Nadu",
                "phone": "+91-44-2829-4004",
                "email": "preethi.krishnan@apollodemo.in",
                "consultation_fee": 900.0,
                "rating": 4.6,
                "total_reviews": 178,
                "bio": "Dr. Preethi Krishnan focuses on stroke rehabilitation and cognitive neurology. She trained at JIPMER and leads the neurostroke unit at Apollo Chennai.",
            },
            # Orthopedics
            {
                "name": "Dr. Ramesh Patel",
                "specialty": "Orthopedics",
                "qualification": "MBBS, MS Orthopedics – KEM Hospital Mumbai",
                "experience_years": 20,
                "hospital": "Hinduja Hospital",
                "city": "Mumbai",
                "state": "Maharashtra",
                "phone": "+91-22-2445-5005",
                "email": "ramesh.patel@hindujademo.in",
                "consultation_fee": 800.0,
                "rating": 4.7,
                "total_reviews": 412,
                "bio": "Dr. Ramesh Patel is a senior orthopedic surgeon with 20 years of experience in joint replacement and sports medicine. He has performed over 2,500 hip and knee replacement surgeries.",
            },
            {
                "name": "Dr. Anjali Singh",
                "specialty": "Orthopedics",
                "qualification": "MBBS, MS, MCh – Sports Medicine, AIIMS",
                "experience_years": 8,
                "hospital": "Max Healthcare",
                "city": "Delhi",
                "state": "Delhi",
                "phone": "+91-11-4055-6006",
                "email": "anjali.singh@maxdemo.in",
                "consultation_fee": 700.0,
                "rating": 4.5,
                "total_reviews": 134,
                "bio": "Dr. Anjali Singh specializes in arthroscopic surgery and sports injuries. She is the orthopedic consultant for two national sports federations.",
            },
            # Dermatology
            {
                "name": "Dr. Kavya Reddy",
                "specialty": "Dermatology",
                "qualification": "MBBS, MD Dermatology – Osmania Medical College",
                "experience_years": 9,
                "hospital": "KIMS Hospital",
                "city": "Hyderabad",
                "state": "Telangana",
                "phone": "+91-40-4477-7007",
                "email": "kavya.reddy@kimsdemo.in",
                "consultation_fee": 600.0,
                "rating": 4.8,
                "total_reviews": 267,
                "bio": "Dr. Kavya Reddy is a dermatologist and cosmetologist with expertise in acne management, laser treatments, and hair restoration. She trained at Osmania Medical College.",
            },
            {
                "name": "Dr. Nikhil Desai",
                "specialty": "Dermatology",
                "qualification": "MBBS, DVD, MD – Grant Medical College",
                "experience_years": 14,
                "hospital": "Kokilaben Dhirubhai Ambani Hospital",
                "city": "Mumbai",
                "state": "Maharashtra",
                "phone": "+91-22-3066-8008",
                "email": "nikhil.desai@kokilabendemo.in",
                "consultation_fee": 900.0,
                "rating": 4.6,
                "total_reviews": 198,
                "bio": "Dr. Nikhil Desai specializes in dermato-oncology and clinical dermatology with 14 years of experience. He runs India's first dedicated skin cancer screening clinic.",
            },
            # Pediatrics
            {
                "name": "Dr. Meera Iyer",
                "specialty": "Pediatrics",
                "qualification": "MBBS, DCH, MD Pediatrics – Madras Medical College",
                "experience_years": 16,
                "hospital": "Rainbow Children's Hospital",
                "city": "Bangalore",
                "state": "Karnataka",
                "phone": "+91-80-6766-9009",
                "email": "meera.iyer@rainbowdemo.in",
                "consultation_fee": 700.0,
                "rating": 4.9,
                "total_reviews": 523,
                "bio": "Dr. Meera Iyer is a pediatrician with 16 years of experience in neonatology and childhood development. She has been awarded the Best Pediatrician award by the Karnataka Medical Council.",
            },
            {
                "name": "Dr. Suresh Babu",
                "specialty": "Pediatrics",
                "qualification": "MBBS, MD, Fellowship Pediatric Neurology – PGIMER",
                "experience_years": 11,
                "hospital": "Apollo Cradle",
                "city": "Hyderabad",
                "state": "Telangana",
                "phone": "+91-40-6060-1010",
                "email": "suresh.babu@apollodemo.in",
                "consultation_fee": 650.0,
                "rating": 4.7,
                "total_reviews": 198,
                "bio": "Dr. Suresh Babu is a pediatric neurologist specializing in childhood epilepsy and neurodevelopmental disorders. He trained at PGIMER Chandigarh.",
            },
            # Gynecology
            {
                "name": "Dr. Lalitha Menon",
                "specialty": "Gynecology",
                "qualification": "MBBS, MS OBG – Calicut Medical College",
                "experience_years": 22,
                "hospital": "Lakeshore Hospital",
                "city": "Kolkata",
                "state": "West Bengal",
                "phone": "+91-33-4044-1111",
                "email": "lalitha.menon@lakeshoredemo.in",
                "consultation_fee": 850.0,
                "rating": 4.8,
                "total_reviews": 445,
                "bio": "Dr. Lalitha Menon is a senior gynecologist with 22 years of experience in high-risk obstetrics and minimally invasive gynecological surgeries. She has delivered over 10,000 babies.",
            },
            {
                "name": "Dr. Pooja Agarwal",
                "specialty": "Gynecology",
                "qualification": "MBBS, DGO, MD – Lady Hardinge Medical College",
                "experience_years": 7,
                "hospital": "Cloudnine Hospital",
                "city": "Delhi",
                "state": "Delhi",
                "phone": "+91-11-4044-1212",
                "email": "pooja.agarwal@cloudninedemo.in",
                "consultation_fee": 700.0,
                "rating": 4.6,
                "total_reviews": 156,
                "bio": "Dr. Pooja Agarwal specializes in fertility treatments, laparoscopic surgery, and maternal-fetal medicine. She trained at Lady Hardinge Medical College, Delhi.",
            },
            # Ophthalmology
            {
                "name": "Dr. Ashok Jain",
                "specialty": "Ophthalmology",
                "qualification": "MBBS, MS Ophthalmology, FRCS – Aravind Eye Hospital",
                "experience_years": 25,
                "hospital": "Sankara Nethralaya",
                "city": "Chennai",
                "state": "Tamil Nadu",
                "phone": "+91-44-2811-1313",
                "email": "ashok.jain@sankararademo.in",
                "consultation_fee": 750.0,
                "rating": 4.9,
                "total_reviews": 612,
                "bio": "Dr. Ashok Jain is one of India's leading ophthalmologists with 25 years of experience in cataract surgery, glaucoma management, and retinal disorders. He has performed over 15,000 eye surgeries.",
            },
            {
                "name": "Dr. Swathi Murthy",
                "specialty": "Ophthalmology",
                "qualification": "MBBS, DO, DNB – Narayana Nethralaya",
                "experience_years": 10,
                "hospital": "Narayana Nethralaya",
                "city": "Bangalore",
                "state": "Karnataka",
                "phone": "+91-80-6660-1414",
                "email": "swathi.murthy@narayanademo.in",
                "consultation_fee": 650.0,
                "rating": 4.7,
                "total_reviews": 234,
                "bio": "Dr. Swathi Murthy specializes in refractive surgery and pediatric ophthalmology. She trained at Narayana Nethralaya Bangalore.",
            },
            # Psychiatry
            {
                "name": "Dr. Rahul Bhattacharya",
                "specialty": "Psychiatry",
                "qualification": "MBBS, MD Psychiatry – NIMHANS Bangalore",
                "experience_years": 13,
                "hospital": "Vandrevala Foundation",
                "city": "Mumbai",
                "state": "Maharashtra",
                "phone": "+91-22-1860-1515",
                "email": "rahul.b@vandrevalademo.in",
                "consultation_fee": 1000.0,
                "rating": 4.8,
                "total_reviews": 189,
                "bio": "Dr. Rahul Bhattacharya is a clinical psychiatrist with expertise in mood disorders, anxiety disorders, and addiction psychiatry. He completed his MD from NIMHANS.",
            },
            {
                "name": "Dr. Nandita Roy",
                "specialty": "Psychiatry",
                "qualification": "MBBS, MD, Fellowship Child Psychiatry – Bangalore",
                "experience_years": 8,
                "hospital": "Fortis Healthcare",
                "city": "Kolkata",
                "state": "West Bengal",
                "phone": "+91-33-6627-1616",
                "email": "nandita.roy@fortisdemo.in",
                "consultation_fee": 900.0,
                "rating": 4.6,
                "total_reviews": 112,
                "bio": "Dr. Nandita Roy is a child and adolescent psychiatrist specializing in ADHD, autism spectrum disorders, and learning disabilities.",
            },
            # Oncology
            {
                "name": "Dr. Sanjay Verma",
                "specialty": "Oncology",
                "qualification": "MBBS, MD, DM Medical Oncology – Tata Memorial",
                "experience_years": 19,
                "hospital": "Tata Memorial Hospital",
                "city": "Mumbai",
                "state": "Maharashtra",
                "phone": "+91-22-2417-1717",
                "email": "sanjay.verma@tatademo.in",
                "consultation_fee": 1500.0,
                "rating": 4.9,
                "total_reviews": 478,
                "bio": "Dr. Sanjay Verma is a senior medical oncologist at Tata Memorial Hospital with 19 years of experience in solid tumors, lymphomas, and targeted therapies. He has over 80 publications.",
            },
            {
                "name": "Dr. Deepa Krishnamurthy",
                "specialty": "Oncology",
                "qualification": "MBBS, MD, DNB Oncology – Christian Medical College",
                "experience_years": 11,
                "hospital": "HCG Cancer Centre",
                "city": "Bangalore",
                "state": "Karnataka",
                "phone": "+91-80-4020-1818",
                "email": "deepa.k@hcgdemo.in",
                "consultation_fee": 1200.0,
                "rating": 4.7,
                "total_reviews": 203,
                "bio": "Dr. Deepa Krishnamurthy specializes in breast oncology and gynecological cancers. She trained at Christian Medical College Vellore.",
            },
            # Gastroenterology
            {
                "name": "Dr. Anil Gupta",
                "specialty": "Gastroenterology",
                "qualification": "MBBS, MD, DM Gastroenterology – SMS Hospital",
                "experience_years": 17,
                "hospital": "Medanta – The Medicity",
                "city": "Delhi",
                "state": "Delhi",
                "phone": "+91-124-441-1919",
                "email": "anil.gupta@medantademo.in",
                "consultation_fee": 1100.0,
                "rating": 4.8,
                "total_reviews": 356,
                "bio": "Dr. Anil Gupta is a gastroenterologist with 17 years of expertise in therapeutic endoscopy, liver disease, and IBD management. He trained at SMS Medical College Jaipur.",
            },
            {
                "name": "Dr. Rekha Pillai",
                "specialty": "Gastroenterology",
                "qualification": "MBBS, MD, DM – Sri Ramachandra Institute",
                "experience_years": 9,
                "hospital": "Global Hospital",
                "city": "Chennai",
                "state": "Tamil Nadu",
                "phone": "+91-44-4477-2020",
                "email": "rekha.pillai@globaldemo.in",
                "consultation_fee": 900.0,
                "rating": 4.5,
                "total_reviews": 145,
                "bio": "Dr. Rekha Pillai specializes in endoscopic procedures and hepatology with a focus on viral hepatitis management.",
            },
            # Pulmonology
            {
                "name": "Dr. Farhan Khan",
                "specialty": "Pulmonology",
                "qualification": "MBBS, MD, DNB Pulmonary Medicine – PGI Lucknow",
                "experience_years": 12,
                "hospital": "Yashoda Hospitals",
                "city": "Hyderabad",
                "state": "Telangana",
                "phone": "+91-40-4567-2121",
                "email": "farhan.khan@yashodademo.in",
                "consultation_fee": 800.0,
                "rating": 4.6,
                "total_reviews": 167,
                "bio": "Dr. Farhan Khan specializes in asthma, COPD, and sleep medicine. He trained at PGI Lucknow and has established one of Hyderabad's first dedicated sleep disorder clinics.",
            },
            # Endocrinology
            {
                "name": "Dr. Bharati Shah",
                "specialty": "Endocrinology",
                "qualification": "MBBS, MD, DM Endocrinology – PGI Chandigarh",
                "experience_years": 15,
                "hospital": "Sterling Hospitals",
                "city": "Ahmedabad",
                "state": "Gujarat",
                "phone": "+91-79-4055-2222",
                "email": "bharati.shah@sterlingdemo.in",
                "consultation_fee": 850.0,
                "rating": 4.7,
                "total_reviews": 289,
                "bio": "Dr. Bharati Shah is an endocrinologist specializing in diabetes management, thyroid disorders, and reproductive endocrinology with 15 years of clinical experience.",
            },
            # Nephrology
            {
                "name": "Dr. Krishnamurthy Rajan",
                "specialty": "Nephrology",
                "qualification": "MBBS, MD, DM Nephrology – SGPGI Lucknow",
                "experience_years": 20,
                "hospital": "Manipal Hospital",
                "city": "Bangalore",
                "state": "Karnataka",
                "phone": "+91-80-2502-2323",
                "email": "k.rajan@manipaldemo.in",
                "consultation_fee": 1100.0,
                "rating": 4.8,
                "total_reviews": 334,
                "bio": "Dr. Krishnamurthy Rajan is a nephrologist with 20 years of expertise in chronic kidney disease, dialysis management, and kidney transplantation.",
            },
            # Urology
            {
                "name": "Dr. Prakash Shetty",
                "specialty": "Urology",
                "qualification": "MBBS, MS, MCh Urology – KEM Hospital Mumbai",
                "experience_years": 14,
                "hospital": "Lilavati Hospital",
                "city": "Mumbai",
                "state": "Maharashtra",
                "phone": "+91-22-2675-2424",
                "email": "prakash.shetty@lilavatidemo.in",
                "consultation_fee": 950.0,
                "rating": 4.6,
                "total_reviews": 221,
                "bio": "Dr. Prakash Shetty is a urologist specializing in robotic surgery for prostate cancer, kidney stone management, and male infertility.",
            },
            # Rheumatology
            {
                "name": "Dr. Sudha Krishnan",
                "specialty": "Rheumatology",
                "qualification": "MBBS, MD, DM Rheumatology – Christian Medical College",
                "experience_years": 11,
                "hospital": "Apollo Hospitals",
                "city": "Chennai",
                "state": "Tamil Nadu",
                "phone": "+91-44-2829-2525",
                "email": "sudha.k@apollodemo.in",
                "consultation_fee": 900.0,
                "rating": 4.7,
                "total_reviews": 198,
                "bio": "Dr. Sudha Krishnan is a rheumatologist with expertise in rheumatoid arthritis, lupus, and ankylosing spondylitis. She trained at CMC Vellore.",
            },
            # ENT
            {
                "name": "Dr. Vinay Kumar",
                "specialty": "ENT",
                "qualification": "MBBS, MS ENT, DNB – AIIMS New Delhi",
                "experience_years": 13,
                "hospital": "Medanta – The Medicity",
                "city": "Delhi",
                "state": "Delhi",
                "phone": "+91-124-441-2626",
                "email": "vinay.kumar@medantademo.in",
                "consultation_fee": 750.0,
                "rating": 4.5,
                "total_reviews": 167,
                "bio": "Dr. Vinay Kumar is an ENT surgeon specializing in endoscopic sinus surgery, cochlear implants, and head & neck oncology. He trained at AIIMS New Delhi.",
            },
            # General Medicine
            {
                "name": "Dr. Alok Mishra",
                "specialty": "General Medicine",
                "qualification": "MBBS, MD Internal Medicine – KGMU Lucknow",
                "experience_years": 16,
                "hospital": "Sahara Hospital",
                "city": "Pune",
                "state": "Maharashtra",
                "phone": "+91-20-4660-2727",
                "email": "alok.mishra@saharademo.in",
                "consultation_fee": 500.0,
                "rating": 4.6,
                "total_reviews": 445,
                "bio": "Dr. Alok Mishra is a general internist with expertise in infectious diseases, hypertension management, and preventive medicine.",
            },
            {
                "name": "Dr. Shalini Kapoor",
                "specialty": "General Medicine",
                "qualification": "MBBS, MD – Maulana Azad Medical College",
                "experience_years": 8,
                "hospital": "Sarvodaya Hospital",
                "city": "Delhi",
                "state": "Delhi",
                "phone": "+91-11-4055-2828",
                "email": "shalini.kapoor@sarvodayademo.in",
                "consultation_fee": 450.0,
                "rating": 4.4,
                "total_reviews": 123,
                "bio": "Dr. Shalini Kapoor is a general physician focusing on lifestyle diseases, diabetes care, and geriatric medicine.",
            },
            # Plastic Surgery
            {
                "name": "Dr. Raghav Malhotra",
                "specialty": "Plastic Surgery",
                "qualification": "MBBS, MS, MCh Plastic Surgery – PGIMER",
                "experience_years": 10,
                "hospital": "Max Healthcare",
                "city": "Delhi",
                "state": "Delhi",
                "phone": "+91-11-4055-2929",
                "email": "raghav.m@maxdemo.in",
                "consultation_fee": 1200.0,
                "rating": 4.7,
                "total_reviews": 156,
                "bio": "Dr. Raghav Malhotra specializes in reconstructive surgery, burn management, and cosmetic procedures. He trained at PGIMER Chandigarh.",
            },
            # Cardiology (Ahmedabad)
            {
                "name": "Dr. Hemant Shah",
                "specialty": "Cardiology",
                "qualification": "MBBS, MD, DM Cardiology – UN Mehta Institute",
                "experience_years": 21,
                "hospital": "UN Mehta Institute of Cardiology",
                "city": "Ahmedabad",
                "state": "Gujarat",
                "phone": "+91-79-2268-3030",
                "email": "hemant.shah@unmehtatdemo.in",
                "consultation_fee": 1000.0,
                "rating": 4.9,
                "total_reviews": 567,
                "bio": "Dr. Hemant Shah is one of Gujarat's foremost cardiologists with expertise in structural heart disease and cardiac electrophysiology.",
            },
            # Neurology (Pune)
            {
                "name": "Dr. Chitra Deshpande",
                "specialty": "Neurology",
                "qualification": "MBBS, MD, DM Neurology – BJ Medical College",
                "experience_years": 14,
                "hospital": "Ruby Hall Clinic",
                "city": "Pune",
                "state": "Maharashtra",
                "phone": "+91-20-6645-3131",
                "email": "chitra.d@rubyhallclinic.in",
                "consultation_fee": 950.0,
                "rating": 4.6,
                "total_reviews": 212,
                "bio": "Dr. Chitra Deshpande specializes in headache disorders, multiple sclerosis, and cognitive neurology. She trained at BJ Medical College, Pune.",
            },
        ]

        doctors = []
        for d in doctors_data:
            doctor = Doctor(**d)
            doctors.append(doctor)
        db.add_all(doctors)
        db.commit()
        print(f"  ✓ Created {len(doctors)} fictional doctors")

        print("\n✅ Seed complete!")
        print("\nDemo Credentials:")
        print("  User:  user@demo.com  / Demo@1234  (150 credits)")
        print("  Admin: admin@demo.com / Admin@1234 (500 credits, admin)")
        print(f"\nDoctors: {len(doctors)} across 10+ specialties and 8 cities")
        print("Packages: Starter / Growth / Professional / Enterprise")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
