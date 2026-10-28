from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Upgrade-ready database of all popular cars running in India
indian_cars_data = {
    'Thar Roxx': {
        'brand': 'Mahindra', 'type': 'SUV', 'price_num': 13, 'price': '₹12.99 Lakh onwards', 'hp': 175, 'top_speed': 165,
        'engine': '2.2L mHawk Diesel / 2.0L mStallion Petrol', 'fuel': 'Diesel / Petrol', 'mileage': 14, 'mileage_str': '12-15 kmpl', 'seats': '5 Seating', 'safety': '5-Star (Bharat NCAP)',
        'img': 'https://c.ndtvimg.com/2025-03/idimpfp_mahindra-thar-roxx_625x300_19_March_25.jpg?im=FeatureCrop,algorithm=dnn,width=1200,height=800',
        'desc': 'The ultimate off-roader with a practical 5-door setup, premium features, and rugged capabilities.'
    },
    'Scorpio-N': {
        'brand': 'Mahindra', 'type': 'SUV', 'price_num': 14, 'price': '₹13.85 Lakh onwards', 'hp': 175, 'top_speed': 170,
        'engine': '2.2L Diesel / 2.0L Turbo Petrol', 'fuel': 'Diesel / Petrol', 'mileage': 14, 'mileage_str': '12-16 kmpl', 'seats': '6 or 7 Seating', 'safety': '5-Star (Global NCAP)',
        'img': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTrliCwX9jlriBi5O8zhj3qhfX_6lQgYMT83jObWcuAuwFzvCKdJxzohYo&s=10',
        'desc': 'The "Big Daddy of SUVs" offers robust body-on-frame build, punchy engines, and commanding road presence.'
    },
    'Scorpio Classic': {
        'brand': 'Mahindra', 'type': 'SUV', 'price_num': 14, 'price': '₹13.62 Lakh onwards', 'hp': 130, 'top_speed': 160,
        'engine': '2.2L mHawk Diesel', 'fuel': 'Diesel Only', 'mileage': 14, 'mileage_str': '13-15 kmpl', 'seats': '7 or 9 Seating', 'safety': 'Updated structural build',
        'img': 'https://www.carandbike.com/_next/image?url=https%3A%2F%2Fimages.carandbike.com%2Fcms%2Farticles%2F2024%2F10%2F3214907%2FScorpio_accessories_8cb80af8b1.jpg&w=1920&q=90',
        'desc': 'The legendary silhouette with the reliable mHawk engine. A true emotion for Indian SUV lovers.'
    },
    'XUV700': {
        'brand': 'Mahindra', 'type': 'SUV', 'price_num': 14, 'price': '₹13.99 Lakh onwards', 'hp': 200, 'top_speed': 190,
        'engine': '2.0L Turbo Petrol / 2.2L Diesel', 'fuel': 'Diesel / Petrol', 'mileage': 15, 'mileage_str': '13-17 kmpl', 'seats': '5 or 7 Seating', 'safety': '5-Star (Global NCAP)',
        'img': 'https://c.ndtvimg.com/2024-07/dg95r5f8_mahindra-xuv700-dark-knight-edition_625x300_09_July_24.jpg?im=FaceCrop,algorithm=dnn,width=1200,height=738',
        'desc': 'Packed with high-tech ADAS features, a beautiful twin-screen setup, and segment-leading power output.'
    },
    'Safari': {
        'brand': 'Tata', 'type': 'SUV', 'price_num': 16, 'price': '₹16.19 Lakh onwards', 'hp': 170, 'top_speed': 175,
        'engine': '2.0L Kryotec Turbocharged Diesel', 'fuel': 'Diesel Only', 'mileage': 15, 'mileage_str': '14-16 kmpl', 'seats': '6 or 7 Seating', 'safety': '5-Star (GNCAP & BNCAP)',
        'img': 'https://5.imimg.com/data5/SELLER/Default/2023/5/306963288/JL/OB/RR/189266364/tata-safari-car.jpg',
        'desc': 'A premium flagship SUV based on the legendary Land Rover D8 platform, offering gold-class comfort and luxury.'
    },
    'Harrier': {
        'brand': 'Tata', 'type': 'SUV', 'price_num': 15, 'price': '₹14.99 Lakh onwards', 'hp': 170, 'top_speed': 180,
        'engine': '2.0L Kryotec Diesel', 'fuel': 'Diesel Only', 'mileage': 15, 'mileage_str': '14-16 kmpl', 'seats': '5 Seating', 'safety': '5-Star (GNCAP)',
        'img': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkBI5OTSRHbTzORqxIkCPLpCy1-9dQKUeXPNoHPRH9hKu6SQGo0wX8fKM&s=10',
        'desc': 'Muscular styling, panoramic sunroof, and a very strong body shell built on Land Rover architecture.'
    },
    'Punch': {
        'brand': 'Tata', 'type': 'Hatchback', 'price_num': 6, 'price': '₹6.13 Lakh onwards', 'hp': 86, 'top_speed': 150,
        'engine': '1.2L Revotron Petrol', 'fuel': 'Petrol / CNG', 'mileage': 19, 'mileage_str': '18-20 kmpl', 'seats': '5 Seating', 'safety': '5-Star (Global NCAP)',
        'img': 'https://imgd.aeplcdn.com/1920x1080/n/cw/ec/172825/punch-exterior-right-front-three-quarter-250.png?isig=0&q=80&q=80',
        'desc': 'Indias super hit micro SUV known for its high ground clearance and exceptional 5-star safety rating.'
    },
    'Nexon EV': {
        'brand': 'Tata', 'type': 'SUV', 'price_num': 12, 'price': '₹12.49 Lakh onwards', 'hp': 143, 'top_speed': 150,
        'engine': 'Permanent Magnet Synchronous Motor', 'fuel': 'Electric', 'mileage': 25, 'mileage_str': '325-465 km Range', 'seats': '5 Seating', 'safety': '5-Star (Global NCAP)',
        'img': 'https://stimg.cardekho.com/images/carexteriorimages/930x620/Tata/Nexon-EV/11024/1755845297648/front-left-side-47.jpg',
        'desc': 'Indias highest selling electric SUV, known for its futuristic cockpit, quiet drive, and great city range.'
    },
    'Virtus GT': {
        'brand': 'Volkswagen', 'type': 'Sedan', 'price_num': 12, 'price': '₹11.55 Lakh onwards', 'hp': 150, 'top_speed': 190,
        'engine': '1.5L TSI EVO Turbo Petrol', 'fuel': 'Petrol Only', 'mileage': 18, 'mileage_str': '18-19 kmpl', 'seats': '5 Seating', 'safety': '5-Star (Global NCAP)',
        'img': 'https://grouplandmark.in/media/1767603084369-exterior-image-168.jpg',
        'desc': 'A pure enthusiast car. Known for stunning German engineering, high-speed stability, and lightning-fast DSG gearbox.'
    },
    'Verna Turbo': {
        'brand': 'Hyundai', 'type': 'Sedan', 'price_num': 11, 'price': '₹11.00 Lakh onwards', 'hp': 160, 'top_speed': 210,
        'engine': '1.5L Turbo GDi Petrol', 'fuel': 'Petrol Only', 'mileage': 19, 'mileage_str': '18-20 kmpl', 'seats': '5 Seating', 'safety': '5-Star (Global NCAP)',
        'img': 'https://imgd.aeplcdn.com/1920x1080/n/cw/ec/204398/verna-exterior-right-front-three-quarter.png?isig=0&q=80&q=80',
        'desc': 'Futuristic design loaded with ventilated seats, Level 2 ADAS, and an extremely aggressive turbo engine.'
    },
    'Creta': {
        'brand': 'Hyundai', 'type': 'SUV', 'price_num': 11, 'price': '₹11.00 Lakh onwards', 'hp': 115, 'top_speed': 170,
        'engine': '1.5L Petrol / 1.5L Diesel / 1.5L Turbo', 'fuel': 'Diesel / Petrol', 'mileage': 19, 'mileage_str': '17-21 kmpl', 'seats': '5 Seating', 'safety': '5-Star expected',
        'img': 'https://stimg.cardekho.com/images/carexteriorimages/930x620/Hyundai/Creta/8667/1755765115423/front-left-side-47.jpg',
        'desc': 'The undisputed king of compact SUVs in India. Offers unbeatable resale value, panoramic sunroof, and premium features.'
    },
    'Fortuner': {
        'brand': 'Toyota', 'type': 'SUV', 'price_num': 34, 'price': '₹33.43 Lakh onwards', 'hp': 201, 'top_speed': 180,
        'engine': '2.8L Powerful Diesel Engine', 'fuel': 'Diesel / Petrol', 'mileage': 12, 'mileage_str': '10-14 kmpl', 'seats': '7 Seating', 'safety': '5-Star (ASEAN NCAP)',
        'img': 'https://upload.wikimedia.org/wikipedia/commons/6/66/2015_Toyota_Fortuner_%28New_Zealand%29.jpg',
        'desc': 'The status symbol of Indian roads. Unmatched reliability, brilliant 4x4 capability, and massive resale value.'
    },
    'Innova Hycross': {
        'brand': 'Toyota', 'type': 'SUV', 'price_num': 20, 'price': '₹19.77 Lakh onwards', 'hp': 184, 'top_speed': 175,
        'engine': '2.0L Petrol Strong Hybrid', 'fuel': 'Petrol Hybrid', 'mileage': 22, 'mileage_str': '21-23 kmpl', 'seats': '7 or 8 Seating', 'safety': '5-Star expected',
        'img': 'https://www.team-bhp.com/sites/default/files/styles/amp_high_res/public/Toyota%20Innova%20Hycross%20Ownership%20review.png',
        'desc': 'Ultra luxurious MPV with ottoman seats and a highly efficient strong hybrid engine that gives stellar mileage.'
    },
    'Grand Vitara': {
        'brand': 'Maruti Suzuki', 'type': 'SUV', 'price_num': 11, 'price': '₹10.99 Lakh onwards', 'hp': 103, 'top_speed': 160,
        'engine': '1.5L Smart Hybrid / Strong Hybrid', 'fuel': 'Petrol / CNG', 'mileage': 24, 'mileage_str': '21-27.9 kmpl', 'seats': '5 Seating', 'safety': 'Built on Suzuki TECT platform',
        'img': 'https://imgd.aeplcdn.com/1056x594/n/lfaq33a_1591831.jpg?q=80',
        'desc': 'Excellent mid-SUV option by Maruti with optional AWD (All-Wheel Drive) and top-notch fuel efficiency.'
    },
    'Swift': {
        'brand': 'Maruti Suzuki', 'type': 'Hatchback', 'price_num': 6, 'price': '₹6.49 Lakh onwards', 'hp': 80, 'top_speed': 165,
        'engine': '1.2L Z-Series Petrol', 'fuel': 'Petrol Only', 'mileage': 24, 'mileage_str': '24-25 kmpl', 'seats': '5 Seating', 'safety': '4-Star (Japan NCAP)',
        'img': 'https://cdn-s3.autocarindia.com/legacy/cdni/mmv_images/colors/20251016103232_Maruti_Suzuki_Swift_Bluish_Black.jpg?w=728&q=75',
        'desc': 'The favorite hatchback of India, now in a brand new avatar with outstanding mileage and sporty dynamics.'
    },
    'Baleno': {
        'brand': 'Maruti Suzuki', 'type': 'Hatchback', 'price_num': 7, 'price': '₹6.66 Lakh onwards', 'hp': 88, 'top_speed': 160,
        'engine': '1.2L DualJet Petrol', 'fuel': 'Petrol / CNG', 'mileage': 26, 'mileage_str': '22-30 kmpl', 'seats': '5 Seating', 'safety': 'Equipped with 6 Airbags',
        'img': 'https://www.carstudiomohali.com/wp-content/uploads/2025/07/Baleno-Car-Price-in-Chandigarh.webp',
        'desc': 'A premium, highly spacious hatchback loaded with a Head-Up Display (HUD) and 360-degree camera.'
    },
    'Elevate': {
        'brand': 'Honda', 'type': 'SUV', 'price_num': 12, 'price': '₹11.69 Lakh onwards', 'hp': 119, 'top_speed': 165,
        'engine': '1.5L i-VTEC Petrol', 'fuel': 'Petrol Only', 'mileage': 16, 'mileage_str': '15-17 kmpl', 'seats': '5 Seating', 'safety': 'Built on high integrity body',
        'img': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQaht-v1PeLEZHPdcdNpiu0BhDjMJxAMtMPT2mTMOKVTA&s=10',
        'desc': 'Hondas reliable mid-size SUV featuring a super smooth i-VTEC engine and best-in-class boot space.'
    },
    'Compass': {
        'brand': 'Jeep', 'type': 'SUV', 'price_num': 21, 'price': '₹20.69 Lakh onwards', 'hp': 168, 'top_speed': 190,
        'engine': '2.0L Multijet Diesel', 'fuel': 'Diesel Only', 'mileage': 15, 'mileage_str': '14-16 kmpl', 'seats': '5 Seating', 'safety': '5-Star (Euro NCAP)',
        'img': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSRuVqsoe_RMsO5-Axd2MjESDfRE0VIFS4XQLJH2-AQ2w&s=10',
        'desc': 'Premium American SUV build quality with hardcore off-roading capabilities and sophisticated interiors.'
    },
    'Thar 3-Door': {
        'brand': 'Mahindra', 'type': 'SUV', 'price_num': 11, 'price': '₹11.35 Lakh onwards', 'hp': 150, 'top_speed': 155,
        'engine': '2.0L mStallion Petrol / 2.2L mHawk Diesel', 'fuel': 'Diesel / Petrol', 'mileage': 12, 'mileage_str': '11-13 kmpl', 'seats': '4 Seating', 'safety': '4-Star (Global NCAP)',
        'img': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQYr_zGnM439ACqHnD50moW82I-ZCzJVrTGqyfiOVcihKastArTYgbonJkP&s=10',
        'desc': 'The iconic 3-door off-roader that redefined lifestyle SUVs in India with unmatched road presence.'
    },
    'XUV 3XO': {
        'brand': 'Mahindra', 'type': 'SUV', 'price_num': 7, 'price': '₹7.49 Lakh onwards', 'hp': 130, 'top_speed': 160,
        'engine': '1.2L Turbo Petrol / 1.5L Diesel', 'fuel': 'Diesel / Petrol', 'mileage': 18, 'mileage_str': '17-20 kmpl', 'seats': '5 Seating', 'safety': '5-Star expected',
        'img': 'https://img.gaadicdn.com/images/car-images/large/Mahindra/XUV-3XO/10184/1714405352406/224_Galaxy-Grey_666a72.jpg',
        'desc': 'Futuristic compact SUV packed with a panoramic skyroof, Level 2 ADAS, and direct-injection turbo power.'
    },
    'Nexon': {
        'brand': 'Tata', 'type': 'SUV', 'price_num': 8, 'price': '₹7.99 Lakh onwards', 'hp': 120, 'top_speed': 170,
        'engine': '1.2L Turbo Petrol / 1.5L Diesel', 'fuel': 'Diesel / Petrol', 'mileage': 17, 'mileage_str': '17-24 kmpl', 'seats': '5 Seating', 'safety': '5-Star (GNCAP & BNCAP)',
        'img': 'https://imgd.aeplcdn.com/1056x594/n/4a9to8b_1933956.jpg?q=80',
        'desc': 'One of Indias safest compact SUVs featuring a fighter-jet inspired cockpit and multiple drive modes.'
    },
    'Altroz': {
        'brand': 'Tata', 'type': 'Hatchback', 'price_num': 6, 'price': '₹6.65 Lakh onwards', 'hp': 110, 'top_speed': 160,
        'engine': '1.2L i-Turbo / 1.5L Diesel / 1.2L CNG', 'fuel': 'Petrol / Diesel / CNG', 'mileage': 19, 'mileage_str': '18-23 kmpl', 'seats': '5 Seating', 'safety': '5-Star (Global NCAP)',
        'img': 'https://cdn.carhp.in/tata/tata_altroz_arcade_grey.jpg?format=webp&width=800&q=75',
        'desc': 'The gold standard of hatchbacks, offering laser-cut design, supreme high-speed stability, and top-tier safety.'
    },
    'Curvv': {
        'brand': 'Tata', 'type': 'SUV', 'price_num': 10, 'price': '₹9.99 Lakh onwards', 'hp': 125, 'top_speed': 175,
        'engine': '1.2L Hyperion Turbo Petrol / 1.5L Kryojet Diesel', 'fuel': 'Diesel / Petrol', 'mileage': 16, 'mileage_str': '15-18 kmpl', 'seats': '5 Seating', 'safety': '5-Star expected',
        'img': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSv5CPd3qr2SChdyCBLH7753Wg5YUl11B77ENZguedDwaQD3UivZNi0jaM&s=10',
        'desc': 'An eye-catching SUV-Coupe with a sloping roofline, powered tailgate, and advanced flush door handles.'
    },
    'Fronx': {
        'brand': 'Maruti Suzuki', 'type': 'SUV', 'price_num': 7, 'price': '₹7.51 Lakh onwards', 'hp': 100, 'top_speed': 165,
        'engine': '1.0L Boosterjet Turbo / 1.2L DualJet', 'fuel': 'Petrol / CNG', 'mileage': 21, 'mileage_str': '20-28 kmpl', 'seats': '5 Seating', 'safety': 'Built on HEARTECT platform',
        'img': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTygd9hMIXHS-UmcarNrgdxGKtt9RvGIkSZobLpHAdjy20XJChGoywvwcE&s=10',
        'desc': 'A sporty crossover SUV with Grand Vitara inspired looks, aerodynamic silhouette, and a punchy turbo engine.'
    },
    'Breza': {
        'brand': 'Maruti Suzuki', 'type': 'SUV', 'price_num': 8, 'price': '₹8.34 Lakh onwards', 'hp': 103, 'top_speed': 160,
        'engine': '1.5L K15C Smart Hybrid', 'fuel': 'Petrol / CNG', 'mileage': 19, 'mileage_str': '17-25 kmpl', 'seats': '5 Seating', 'safety': '4-Star expected (GNCAP)',
        'img': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSI2iTqUPnp1V4mILTiLmFbObtqbI65IVbgS0OtPTLl4A&s=10',
        'desc': 'A highly reliable compact SUV known for its muscular boxy design, electric sunroof, and massive cabin space.'
    },
    'Dzire': {
        'brand': 'Maruti Suzuki', 'type': 'Sedan', 'price_num': 6, 'price': '₹6.57 Lakh onwards', 'hp': 90, 'top_speed': 160,
        'engine': '1.2L K-Series Petrol', 'fuel': 'Petrol / CNG', 'mileage': 23, 'mileage_str': '22-31 kmpl', 'seats': '5 Seating', 'safety': '2-Star (Previous GNCAP)',
        'img': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQsGrN7HL8BHPk8n-j0hBa-C_2cCr4unp72DvjJPPgyL7R18D0aR5R9Upw&s=10',
        'desc': 'Indias highest selling compact sedan, offering absolute peace of mind, low maintenance, and stellar mileage.'
    },
    'Exter': {
        'brand': 'Hyundai', 'type': 'SUV', 'price_num': 6, 'price': '₹6.13 Lakh onwards', 'hp': 83, 'top_speed': 150,
        'engine': '1.2L Kappa Petrol', 'fuel': 'Petrol / CNG', 'mileage': 19, 'mileage_str': '19-27 kmpl', 'seats': '5 Seating', 'safety': '6 Airbags Standard',
        'img': 'https://cdn-s3.autocarindia.com/legacy/cdni/ExtraImages/20230508122258_Exter.jpg',
        'desc': 'An outdoor-focused micro SUV fitted with a factory-installed dashcam, sunroof, and modern parametric design.'
    },
    'City': {
        'brand': 'Honda', 'type': 'Sedan', 'price_num': 11, 'price': '₹11.82 Lakh onwards', 'hp': 121, 'top_speed': 180,
        'engine': '1.5L i-VTEC Petrol / 1.5L Hybrid Atkinson', 'fuel': 'Petrol / Hybrid', 'mileage': 18, 'mileage_str': '17-27 kmpl', 'seats': '5 Seating', 'safety': '5-Star (ASEAN NCAP)',
        'img': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/134287/city-exterior-right-front-three-quarter-2.png?isig=0&q=80',
        'desc': 'The benchmark of premium executive sedans in India for over two decades. Renowned for its plush ride quality.'
    },
    'BMW 3 Series Gran Limousine': {
        'brand': 'BMW', 'type': 'Sedan', 'price_num': 60, 'price': '₹60.60 Lakh onwards', 'hp': 250, 'top_speed': 250,
        'engine': '2.0L TwinPower Turbo 4-Cylinder', 'fuel': 'Petrol / Diesel', 'mileage': 15, 'mileage_str': '13-19 kmpl', 'seats': '5 Seating', 'safety': '5-Star (Euro NCAP)',
        'img': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRI9pGo6uhhah3M1pYBHB35rJowXeCvM0c2gO-RR-aFA7RU9AM2MjV2JK70&s=10',
        'desc': 'The perfect blend of luxury and driving dynamics, offering extra legroom and a sporty cockpit.'
    },
    'BMW X1': {
        'brand': 'BMW', 'type': 'SUV', 'price_num': 49, 'price': '₹49.50 Lakh onwards', 'hp': 148, 'top_speed': 210,
        'engine': '1.5L 3-Cylinder Petrol / 2.0L 4-Cylinder Diesel', 'fuel': 'Diesel / Petrol', 'mileage': 16, 'mileage_str': '15-20 kmpl', 'seats': '5 Seating', 'safety': '5-Star (Euro NCAP)',
        'img': 'https://imgd.aeplcdn.com/1920x1080/n/cw/ec/140591/x1-exterior-right-front-three-quarter-8.png?isig=0&q=80&q=80',
        'desc': 'BMWs highest selling luxury compact SUV in India. Bold styling, futuristic curved display, and agile handling.'
    },
    'Mercedes-Benz C-Class': {
        'brand': 'Mercedes-Benz', 'type': 'Sedan', 'price_num': 61, 'price': '₹61.85 Lakh onwards', 'hp': 201, 'top_speed': 245,
        'engine': '1.5L Turbo Petrol / 2.0L Diesel with Mild Hybrid', 'fuel': 'Petrol / Diesel Hybrid', 'mileage': 16, 'mileage_str': '14-17 kmpl', 'seats': '5 Seating', 'safety': '5-Star (Euro NCAP)',
        'img': 'https://cdn-s3.autocarindia.com/legacy/cdni/mmv_images/colors/20250704055231_Mercedes_Benz_C_Class_Obsidian_Black[1].png?w=640',
        'desc': 'Often called the "Baby S-Class". Packed with a massive vertical touchscreen, ambient lighting, and unmatched luxury feel.'
    },
    'Mercedes-Benz GLA': {
        'brand': 'Mercedes-Benz', 'type': 'SUV', 'price_num': 51, 'price': '₹51.75 Lakh onwards', 'hp': 163, 'top_speed': 210,
        'engine': '1.3L Turbo Petrol / 2.0L Diesel', 'fuel': 'Diesel / Petrol', 'mileage': 15, 'mileage_str': '14-18 kmpl', 'seats': '5 Seating', 'safety': '5-Star (Euro NCAP)',
        'img': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTCJIOSbY_fCoox0HazhtvNAdsbz3Ct5MF-W2lVNzA-BOEoutjGTuBDqvtP&s=10',
        'desc': 'A stylish, high-riding luxury crossover with the advanced MBUX infotainment system and sporty looks.'
    },
    'Audi A4': {
        'brand': 'Audi', 'type': 'Sedan', 'price_num': 46, 'price': '₹46.02 Lakh onwards', 'hp': 190, 'top_speed': 240,
        'engine': '2.0L TFSI Turbo Petrol', 'fuel': 'Petrol Only', 'mileage': 17, 'mileage_str': '17.4 kmpl', 'seats': '5 Seating', 'safety': '5-Star (Euro NCAP)',
        'img': 'https://imgd.aeplcdn.com/1920x1080/n/cw/ec/51909/a4-exterior-right-front-three-quarter-80.png?isig=0&q=80&q=80',
        'desc': 'Audias executive sedan known for its extremely smooth ride quality, Virtual Cockpit, and understated class.'
    },
    'Audi Q3': {
        'brand': 'Audi', 'type': 'SUV', 'price_num': 44, 'price': '₹44.25 Lakh onwards', 'hp': 190, 'top_speed': 220,
        'engine': '2.0L 4-Cylinder TFSI Petrol', 'fuel': 'Petrol Only', 'mileage': 14, 'mileage_str': '12-15 kmpl', 'seats': '5 Seating', 'safety': '5-Star (Euro NCAP)',
        'img': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmxnlbgprMCwV53ArAqfolkuEy6IrbnOnBRLFexWH_sg&s=10',
        'desc': 'A sporty family SUV featuring Audias legendary Quattro all-wheel-drive system and muscular road presence.'
    },
    'BMW M4 Competition': {
        'brand': 'BMW', 'type': 'Sedan', 'price_num': 153, 'price': '₹1.53 Crore onwards', 'hp': 510, 'top_speed': 250,
        'engine': '3.0L M TwinPower Turbo Inline 6', 'fuel': 'Petrol Only', 'mileage': 10, 'mileage_str': '9-11 kmpl', 'seats': '4 Seating', 'safety': '5-Star (Euro NCAP)',
        'img': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT7AtgSVL_svKhw0YVZj0IcIpzuf2MKbt9m7eNbf8tJCiw0YmoFPp9yqlPC&s=10',
        'desc': 'A hardcore, track-focused luxury sports coupe with aggressive styling, carbon fiber bits, and blistering acceleration.'
    },
    'BMW X5': {
        'brand': 'BMW', 'type': 'SUV', 'price_num': 97, 'price': '₹97.00 Lakh onwards', 'hp': 375, 'top_speed': 250,
        'engine': '3.0L TwinPower Turbo 6-Cylinder', 'fuel': 'Petrol / Diesel', 'mileage': 12, 'mileage_str': '11-13 kmpl', 'seats': '5 Seating', 'safety': '5-Star (Euro NCAP)',
        'img': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/152681/x5-facelift-exterior-right-front-three-quarter-2.jpeg',
        'desc': 'The ultimate luxury executive SUV, offering a commanding road presence, split tailgate, and supreme highway cruising comfort.'
    },
    'BMW iX': {
        'brand': 'BMW', 'type': 'SUV', 'price_num': 140, 'price': '₹1.40 Crore onwards', 'hp': 326, 'top_speed': 200,
        'engine': 'Dual Electric Motors (76.6 kWh Battery)', 'fuel': 'Electric', 'mileage': 425, 'mileage_str': '425 km Range/Charge', 'seats': '5 Seating', 'safety': '5-Star (Euro NCAP)',
        'img': 'https://imgd.aeplcdn.com/1920x1080/n/cw/ec/108499/ix-exterior-right-front-three-quarter-4.png?isig=0&q=80&q=80',
        'desc': 'BMWs flagship electric SUV. Features a futuristic lounge-like interior, eco-friendly materials, and lounge seats.'
    },
    'BMW 7 Series': {
        'brand': 'BMW', 'type': 'Sedan', 'price_num': 182, 'price': '₹1.82 Crore onwards', 'hp': 381, 'top_speed': 250,
        'engine': '3.0L Inline 6 Turbo Petrol / Diesel', 'fuel': 'Petrol / Diesel', 'mileage': 13, 'mileage_str': '12-15 kmpl', 'seats': '5 Seating', 'safety': '5-Star (Euro NCAP)',
        'img': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSPxgIaaxZzmJL99pXmlr0100i3Kh_hoJYF1Kbmv86KKi5AtQeS-f1QwsM&s=10',
        'desc': 'The peak of BMW luxury. It comes with a massive 31.3-inch 8K theater screen for rear passengers and automatic doors.'
    },
    'Fortuner': {
        'brand': 'Toyota', 'type': 'SUV', 'price_num': 33, 'price': '₹33.43 Lakh onwards', 'hp': 201, 'top_speed': 190,
        'engine': '2.7L Petrol / 2.8L Turbo Diesel', 'fuel': 'Diesel / Petrol', 'mileage': 10, 'mileage_str': '10-14 kmpl', 'seats': '7 Seating', 'safety': '5-Star (ASEAN NCAP)',
        'img': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/44709/fortuner-exterior-right-front-three-quarter-20.jpeg',
        'desc': 'The undisputed king of full-size SUVs in India. Known for its massive road presence, high resale value, and legendary off-road capability.'
    },
    'Innova Hycross': {
        'brand': 'Toyota', 'type': 'SUV', 'price_num': 20, 'price': '₹19.77 Lakh onwards', 'hp': 184, 'top_speed': 175,
        'engine': '2.0L 4-Cylinder Petrol / 2.0L Self-Charging Hybrid', 'fuel': 'Petrol / Strong Hybrid', 'mileage': 23, 'mileage_str': '16-23 kmpl', 'seats': '7-8 Seating', 'safety': '5-Star expected',
        'img': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/115025/innova-hycross-exterior-right-front-three-quarter-73.jpeg',
        'desc': 'A futuristic MPV with SUV styling. It offers ottoman seats in the middle row, a panoramic sunroof, and incredible hybrid fuel efficiency.'
    },
    'Glanza': {
        'brand': 'Toyota', 'type': 'Hatchback', 'price_num': 7, 'price': '₹6.86 Lakh onwards', 'hp': 89, 'top_speed': 160,
        'engine': '1.2L DualJet Petrol', 'fuel': 'Petrol / CNG', 'mileage': 22, 'mileage_str': '22-30 kmpl', 'seats': '5 Seating', 'safety': 'Built on HEARTECT platform',
        'img': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/112839/glanza-exterior-right-front-three-quarter-5.jpeg',
        'desc': 'A premium, feature-loaded hatchback designed for daily city commutes. Comes with a heads-up display and a 360-degree camera.'
    },
    'Urban Cruiser Taisor': {
        'brand': 'Toyota', 'type': 'SUV', 'price_num': 8, 'price': '₹7.74 Lakh onwards', 'hp': 100, 'top_speed': 165,
        'engine': '1.2L Petrol / 1.0L Turbo Petrol', 'fuel': 'Petrol / CNG', 'mileage': 21, 'mileage_str': '20-28 kmpl', 'seats': '5 Seating', 'safety': '6 Airbags on top variants',
        'img': 'https://ackodrive-prod.ackoassets.com/image/toyota/urban-cruiser-taisor/cafe-white-with-midnight-black-roof/images_cdn/small/Transparent.webp',
        'desc': 'Toyotas latest aerodynamic compact crossover with a sporty slope-back design, punchy performance, and aggressive front grille.'
    },
    'Hilux': {
        'brand': 'Toyota', 'type': 'SUV', 'price_num': 30, 'price': '₹30.40 Lakh onwards', 'hp': 201, 'top_speed': 175,
        'engine': '2.8L Turbo Diesel 4x4', 'fuel': 'Diesel Only', 'mileage': 12, 'mileage_str': '10-12 kmpl', 'seats': '5 Seating', 'safety': '5-Star (ASEAN NCAP)',
        'img': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/109265/hilux-exterior-right-front-three-quarter-2.jpeg',
        'desc': 'A heavy-duty lifestyle utility pickup truck. Built on the indestructible IMV platform with heavy water-wading capacity.'
    },
    'Amaze': {
        'brand': 'Honda', 'type': 'Sedan', 'price_num': 7, 'price': '₹7.20 Lakh onwards', 'hp': 90, 'top_speed': 160,
        'engine': '1.2L i-VTEC Petrol', 'fuel': 'Petrol Only', 'mileage': 18, 'mileage_str': '18-19 kmpl', 'seats': '5 Seating', 'safety': '4-Star (Global NCAP)',
        'img': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-UV8bYyts45UyNzWK_ab7Qfy_C3BrLDOlHQIB60KlqQ&s=10',
        'desc': 'A highly comfortable compact sedan with a big boot, smooth CVT automatic option, and low maintenance.'
    },
    'City Hybrid (e:HEV)': {
        'brand': 'Honda', 'type': 'Sedan', 'price_num': 19, 'price': '₹19.00 Lakh onwards', 'hp': 126, 'top_speed': 176,
        'engine': '1.5L Atkinson Cycle Petrol with Dual Electric Motors', 'fuel': 'Strong Hybrid', 'mileage': 27, 'mileage_str': '26-27 kmpl', 'seats': '5 Seating', 'safety': '5-Star (ASEAN NCAP) & ADAS',
        'img': 'https://imgd.aeplcdn.com/664x374/n/cw/ec/143275/city-hybrid-exterior-right-front-three-quarter-6.png?isig=0&q=80',
        'desc': 'An advanced self-charging hybrid sedan that delivers stellar diesel-like fuel economy with pure petrol refinement.'
    },
    'Meridian': {
        'brand': 'Jeep', 'type': 'SUV', 'price_num': 33, 'price': '₹33.60 Lakh onwards', 'hp': 170, 'top_speed': 198,
        'engine': '2.0L Multijet Turbo Diesel', 'fuel': 'Diesel Only', 'mileage': 15, 'mileage_str': '15-16 kmpl', 'seats': '7 Seating', 'safety': '6 Airbags Standard',
        'img': 'Meridian',
        'desc': 'A premium 3-row, 7-seater SUV built on the Compass platform. Offers impressive highway stability and a plush ride.'
    },
    'Wrangler': {
        'brand': 'Jeep', 'type': 'SUV', 'price_num': 67, 'price': '₹67.65 Lakh onwards', 'hp': 270, 'top_speed': 180,
        'engine': '2.0L 4-Cylinder Turbo Petrol', 'fuel': 'Petrol Only', 'mileage': 11, 'mileage_str': '10-12 kmpl', 'seats': '5 Seating', 'safety': 'Highly durable roll-cage structure',
        'img': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRCjSpMgfLI61nKDJhkjHruI1atBYM8VL95s3GFNohY5Q&s=10',
        'desc': 'The ultimate go-anywhere off-road icon. It features removable doors, a fold-down windshield, and the legendary 4x4 Selec-Trac system.'
    },
    'Grand Cherokee': {
        'brand': 'Jeep', 'type': 'SUV', 'price_num': 80, 'price': '₹80.50 Lakh onwards', 'hp': 272, 'top_speed': 210,
        'engine': '2.0L Turbo Petrol with 8-Speed Automatic', 'fuel': 'Petrol Only', 'mileage': 9, 'mileage_str': '8-10 kmpl', 'seats': '5 Seating', 'safety': '5-Star (Euro NCAP) & ADAS',
        'img': 'https://stimg.cardekho.com/images/carexteriorimages/930x620/Jeep/Grand-Cherokee/10945/1767782308966/front-left-side-47.jpg',
        'desc': 'Jeeps flagship luxury SUV in India. It packs a passenger-side screen, Capri leather seats, and Quadra-Lift air suspension.'
    },
    'Mercedes-Benz E-Class': {
        'brand': 'Mercedes-Benz', 'type': 'Sedan', 'price_num': 76, 'price': '₹76.05 Lakh onwards', 'hp': 194, 'top_speed': 240,
        'engine': '2.0L 4-Cylinder Petrol / 2.0L Diesel', 'fuel': 'Petrol / Diesel', 'mileage': 15, 'mileage_str': '13-15 kmpl', 'seats': '5 Seating', 'safety': '5-Star (Euro NCAP)',
        'img': 'https://stimg.cardekho.com/images/carexteriorimages/930x620/Mercedes-Benz/E-Class/9790/1763471140336/front-left-side-47.jpg',
        'desc': 'The undisputed boss of luxury executive sedans. Known for its long wheelbase, rear-seat comfort, and chilling ambient lighting.'
    },
    'Mercedes-Benz GLE': {
        'brand': 'Mercedes-Benz', 'type': 'SUV', 'price_num': 96, 'price': '₹96.40 Lakh onwards', 'hp': 269, 'top_speed': 230,
        'engine': '2.0L Diesel / 3.0L 6-Cylinder Petrol & Diesel', 'fuel': 'Diesel / Petrol Hybrid', 'mileage': 12, 'mileage_str': '10-14 kmpl', 'seats': '5 Seating', 'safety': '5-Star (Euro NCAP)',
        'img': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSAfmwO8LT7wVgnzRrsehsiJLynLC26bxQ48bS6pDMQ2A&s=10',
        'desc': 'A heavy-duty luxury SUV that combines raw power with a high-tech cabin, featuring Transparent Bonnet tech for off-roading.'
    },
    'Audi A6': {
        'brand': 'Audi', 'type': 'Sedan', 'price_num': 64, 'price': '₹64.41 Lakh onwards', 'hp': 241, 'top_speed': 250,
        'engine': '2.0L TFSI Turbo Petrol', 'fuel': 'Petrol Only', 'mileage': 14, 'mileage_str': '14.1 kmpl', 'seats': '5 Seating', 'safety': '5-Star (Euro NCAP)',
        'img': 'https://stimg.cardekho.com/images/carexteriorimages/930x620/Audi/A6/10552/1700631019657/front-view-118.jpg',
        'desc': 'A sleek, tech-forward luxury sedan equipped with a dual-touchscreen dashboard and a futuristic Matrix LED headlight setup.'
    },
    'Audi Q7': {
        'brand': 'Audi', 'type': 'SUV', 'price_num': 88, 'price': '₹88.66 Lakh onwards', 'hp': 340, 'top_speed': 250,
        'engine': '3.0L V6 TFSI Petrol with Mild Hybrid', 'fuel': 'Petrol Hybrid', 'mileage': 11, 'mileage_str': '11.2 kmpl', 'seats': '7 Seating', 'safety': '5-Star (Euro NCAP)',
        'img': 'https://imgd.aeplcdn.com/1920x1080/n/cw/ec/192279/q7-exterior-right-front-three-quarter-3.jpeg?isig=0&q=80&q=80',
        'desc': 'The legendary 7-seater luxury fortress. Packs a massive V6 engine, Quattro AWD, and a panoramic view that gives true king-size vibes.'
    }
}

@app.route('/')
def home():
    car_list = sorted(list(indian_cars_data.keys()))
    return render_template('index.html', car_names=car_list)

@app.route('/get_data', methods=['POST'])
def get_data():
    selected_car = request.json.get('car_name')
    if selected_car in indian_cars_data:
        return jsonify({'status': 'success', 'data': indian_cars_data[selected_car]})
    return jsonify({'status': 'error', 'message': 'Car not found'})

# New route for advanced features (charts, comparisons, and filters)
@app.route('/get_all_data', methods=['GET'])
def get_all_data():
    return jsonify(indian_cars_data)

if __name__ == '__main__':
    app.run(debug=True, port=5002)