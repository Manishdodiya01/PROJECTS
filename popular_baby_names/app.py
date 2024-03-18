from flask import Flask , render_template , request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split , cross_val_score , GridSearchCV , RandomizedSearchCV
from sklearn.preprocessing import LabelEncoder , OneHotEncoder , StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBRFClassifier , XGBClassifier
from sklearn.ensemble import VotingClassifier , RandomForestClassifier , GradientBoostingClassifier
from sklearn.metrics import confusion_matrix , accuracy_score , classification_report
from sklearn.pipeline import make_pipeline , Pipeline
from sklearn.compose import ColumnTransformer , make_column_transformer
import joblib


model = joblib.load('artifacts/Xgb_model.joblib')
preprocessor = joblib.load('artifacts/preprocessor__.joblib')

app = Flask(__name__)

@app.route('/')
def home():
    counts = [ 13,  21,  49,  38,  36,  26, 126,  14,  17,  10,  15,  16,  11,
        28, 331,  18,  27,  23,  30,  50,  12,  20,  41,  33,  51,  22,
        24,  59,  46,  31,  25,  60,  62,  83,  19,  57, 103,  37,  29,
        52, 123,  66, 122,  32, 109, 229,  71,  86, 100,  53,  65, 165,
       223,  85,  45,  42, 114,  54, 162,  40, 132, 127, 178,  95,  35,
        44,  39, 119, 213, 224,  64,  72, 102,  68,  82,  93,  34, 160,
       116, 183,  47,  81,  63,  94, 131, 171, 113,  43,  74, 107, 177,
        48, 180,  69,  84,  96,  70,  98, 173, 110,  92,  76, 150, 167,
        89,  88,  91,  80, 156, 124, 105,  75, 184, 153, 128, 121,  61,
        58, 101, 157, 188, 219,  55, 125, 253, 207, 104,  99, 106,  67,
        78, 176,  90,  87,  77, 190, 151, 239, 221, 136, 158,  73, 303,
       120, 118, 144, 140, 310, 276, 174, 172, 129, 197, 133, 135, 230,
       147, 210, 258,  97, 149, 166, 281,  79, 189, 292,  56, 181, 170,
       251, 426, 265, 111, 159, 161, 186, 117, 327, 236, 155, 148, 137,
       228, 192, 198, 209, 187, 112, 115, 141, 164, 235, 200, 194, 139,
       195, 254, 293, 364, 108, 215, 279, 227, 218, 169, 232, 289, 242,
       300, 168, 245, 238, 185, 206, 352, 212, 399, 175, 182, 266, 257,
       233, 262, 270, 134, 191, 138, 152, 312, 326, 237, 241, 291, 214,
       143, 179, 146, 130, 220, 304, 225, 226, 252, 297, 145, 256, 199,
       217, 244, 283, 193, 216, 255, 259, 205, 248, 204, 282, 272, 268,
       267, 250, 222, 260, 231, 196, 407, 290, 287, 264, 202, 269, 261,
       339, 299, 307, 201, 308, 387, 154, 208, 356, 332, 163, 234, 142,
       351, 211, 423, 285, 274, 246]
    
    child_names = [
        'GERALDINE', 'GIA','GIANNA','GISELLE','GRACE','GUADALUPE','ANTONIO',
 'ARIEL',
 'ARMANDO',
 'ARMANI',
 'ARTURO', 'ASHTON', 'AUSTIN', 'AVERY', 'AXEL', 'AYDEN', 'BENJAMIN', 'BRADLEY', 'BRANDON', 'BRAYAN', 'BRAYDEN', 'Jason', 'BRYAN', 'BRYANT', 'BRYCE', 'BYRON', 'CALEB', 'CAMERON', 'CARLOS', 'CARMELO', 'CESAR', 'ABIGAIL', 'ADA', 'AISHA', 'AIZA', 'ALEENA', 'ALEXA', 'ALEXANDRA', 'ALICE', 'ALINA', 'ALISHA', 'ALIYAH',
 'ALLISON',
 'ALYSSA',
 'AMANDA',
 'AMBER',
 'AMELIA',
 'AMY',
 'ANGEL',
 'ANGELA',
 'ANGELINA', 'ANGIE', 'ANIKA', 'ANNA', 'ANNABELLE', 'ANNIE', 'ARIA', 'ARIANA', 'ARIANNA', 'ARYA', 'ASHLEY', 'AUDREY', 'AVA', 'AYESHA', 'BELLA', 'BONNIE',
 'BRIANNA',
 'CATHERINE',
 'CECILIA',
 'CHARLOTTE',
 'CHLOE',
 'CHRISTINA',
 'CHRISTINE',
 'HAILEY',
 'HALEY',
 'HANNAH',
 'HAYLEE',
 'HAYLEY',
 'HAZEL',
 'HEAVEN',
 'HEIDI',
 'HEIDY', 'HELEN','IMANI',
 'INGRID',
 'IRENE',
 'IRIS',
 'ISABEL',
 'ISABELA',
 'ISABELLA',
 'ISABELLE',
 'ISIS',
 'ITZEL',
 'IZABELLA',
 'JACQUELINE',
 'JADA',
 'JADE',
 'JAELYNN',
 'JAMIE',
 'JANELLE',
 'JASLENE',
 'JASMIN',
 'JASMINE',
 'JAYDA',
 'JAYLA',
 'JAYLAH',
 'JAYLEEN',
 'JAYLENE',
 'JAYLIN',
 'JAYLYN',
 'JAZLYN',
 'JAZMIN',
 'JAZMINE',
 'JENNIFER',
 'JESSICA',
 'JIMENA',
 'JOCELYN',
 'JOHANNA',
 'JOSELYN',
 'JULIA',
 'JULIANA',
 'JULIANNA',
 'JULIET',
 'JULIETTE',
 'JULISSA',
 'KAELYN',
 'KAILEY',
 'KAILYN',
 'KAITLYN',
 'KAMILA',
 'KAREN',
 'KARLA',
 'KATE',
 'KATELYN',
 'KATELYNN',
 'KATHERINE',
 'KATIE',
 'KAYLA',
 'KAYLEE',
 'KAYLEEN',
 'KAYLEIGH',
 'KAYLIE',
 'KAYLIN',
 'KEILY',
 'KELLY',
 'KEYLA',
 'KHLOE',
 'KIARA',
 'KIMBERLY',
 'KRYSTAL',
 'KYLEE',
 'KYLIE',
 'LAILA',
 'LAURA',
 'LAUREN',
 'LAYLA',
 'LEA',
 'LEAH',
 'LEILA',
 'LEILANI',
 'LESLEY',
 'LESLIE',
 'LESLY',
 'LEYLA',
 'LIA',
 'LIANA',
 'LILIANA',
 'LILY',
 'LINDSAY',
 'LIZBETH',
 'LONDON',
 'LUCIA',
 'LUNA',
 'LUZ',
 'MADELINE',
 'MADELYN',
 'MADISON',
 'MAKAYLA',
 'MARIA',
 'MARIAH',
 'MARIANA',
 'MARILYN',
 'MARISOL',
 'MAYA',
 'MEGAN',
 'MELANIE',
 'MELANY',
 'MELISSA',
 'MELODY',
 'MIA',
 'MIAH',
 'MICHELLE',
 'MIKAELA',
 'MIKAYLA',
 'MILA',
 'MILEY',
 'MIRANDA',
 'MIRIAM',
 'MYA',
 'NADIA',
 'NANCY',
 'NAOMI',
 'NATALIA',
 'NATALIE',
 'NATALY',
 'NATASHA',
 'NATHALIA',
 'NATHALIE',
 'NATHALY',
 'NAYELI',
 'NEVAEH',
 'NICOLE',
 'NINA',
 'NOEMI',
 'NYLA',
 'OLIVIA',
 'PAOLA',
 'PENELOPE',
 'PERLA',
 'RACHEL',
 'RAQUEL',
 'REBECCA',
 'RIHANNA',
 'RILEY',
 'ROSA',
 'ROSE',
 'ROSELYN',
 'RUBY',
 'SABRINA',
 'SADIE',
 'SAMANTHA',
 'SAMARA',
 'SARA',
 'SARAH',
 'SARAI',
 'SARIAH',
 'SASHA',
 'SAVANNA',
 'SAVANNAH',
 'SCARLET',
 'SCARLETT',
 'SELENA',
 'SERENITY',
 'SHERLYN',
 'SHIRLEY',
 'SIENNA',
 'SKYLA',
 'SKYLAR',
 'SOFIA',
 'SOPHIA',
 'SOPHIE',
 'STACY',
 'STELLA',
 'STEPHANIE',
 'STEPHANY',
 'TATIANA',
 'TAYLOR',
 'TIANA',
 'TIFFANY',
 'VALENTINA',
 'VALERIA',
 'VALERIE',
 'VANESSA',
 'VERONICA',
 'VICTORIA',
 'VIOLET',
 'VIVIANA',
 'WENDY',
 'XIMENA',
 'YAMILET',
 'YARETZI',
 'ZOE',
 'ZOEY',
 'ABIGAIL',
 'ADDISON',
 'ADELE',
 'ADELINE',
 'ADINA',
 'ADRIANA',
 'ADRIANNA',
 'AHUVA',
 'ALESSANDRA',
 'ALESSIA',
 'ALEXA',
 'ALEXANDRA',
 'ALEXIS',
 'ALICE',
 'ALICIA',
 'ALINA',
 'ALISA',
 'ALIZA',
 'ALLISON',
 'ALYSSA',
 'AMANDA',
 'AMELIA',
 'AMELIE',
 'AMINA',
 'AMIRA',
 'AMY',
 'ANASTASIA',
 'ANGELICA',
 'ANGELINA',
 'ANNA',
 'ANNABEL',
 'ANNABELLE',
 'ARIANA',
 'ARIANNA',
 'ARIEL',
 'ARIELA',
 'ARIELLA',
 'ASHLEY',
 'ATARA',
 'AUBREY',
 'AUDREY',
 'AUTUMN',
 'AVA',
 'AVERY',
 'AVIGAIL',
 'AVIVA',
 'AYLA',
 'BAILA',
 'BARBARA',
 'BATSHEVA',
 'BATYA',
 'BEATRICE',
 'BELLA',
 'BIANCA',
 'BLAKE',
 'BLIMA',
 'BLIMY',
 'BRACHA',
 'BREINDY',
 'BRIANNA',
 'BRIDGET',
 'BROOKE',
 'BROOKLYN',
 'BRUCHA',
 'BRUCHY',
 'BRYNN',
 'CAITLIN',
 'CAMERON',
 'CAROLINE',
 'CASEY',
 'CATHERINE',
 'CECILIA',
 'CELIA',
 'CHANA',
 'CHANY',
 'CHARLIE',
 'CHARLOTTE',
 'CHAVA',
 'CHAVY',
 'CHAYA',
 'CHLOE',
 'CHRISTINA',
 'CLAIRE',
 'CLARA',
 'COLETTE',
 'CORA',
 'DAHLIA',
 'DAISY',
 'DALIA',
 'DANIELA',
 'DANIELLA',
 'DANIELLE',
 'DEVORA',
 'DEVORAH',
 'DIANA',
 'DINA',
 'DYLAN',
 'EDEN',
 'ELEANOR',
 'ELENA',
 'ELIANA',
 'ELISE',
 'ELISHEVA',
 'ELIZA',
 'ELIZABETH',
 'ELLA',
 'ELLE',
 'ELLIANA',
 'ELLIE',
 'ELOISE',
 'EMERSON',
 'EMILIA',
 'EMILY',
 'EMMA',
 'ERIN',
 'ESTER',
 'ESTHER',
 'ESTY',
 'ETTY',
 'EVA',
 'EVE',
 'EVELYN',
 'FAIGA',
 'FAIGY',
 'FINLEY',
 'FIONA',
 'FRADEL',
 'FRAIDY',
 'FRANCESCA',
 'FRIMET',
 'GABRIELA',
 'GABRIELLA',
 'GABRIELLE',
 'GEMMA',
 'GENEVIEVE',
 'GEORGIA',
 'GIA',
 'GIANNA',
 'GIOVANNA',
 'GITTEL',
 'GITTY',
 'GIULIANA',
 'GOLDA',
 'GOLDY',
 'GRACE',
 'GRETA',
 'HADASSA',
 'HADASSAH',
 'HAILEY',
 'HANNA',
 'HANNAH',
 'HARPER',
 'HAZEL',
 'HENNY',
 'HINDY',
 'IDY',
 'ILANA',
 'Jared',
 'ISABEL',
 'ISABELLA',
 'ISABELLE',
 'ISLA',
 'IVY',
 'IZABELLA',
 'JACQUELINE',
 'JANE',
 'JASMINE',
 'JENNA',
 'JESSICA',
 'JORDYN',
 'JOSEPHINE',
 'JOYCE',
 'JULIA',
 'JULIANA',
 'JULIANNA',
 'JULIE',
 'JULIET',
 'JULIETTE',
 'KAITLYN',
 'ARELY',
 'KATE',
 'KATHERINE',
 'KATHRYN',
 'KAYLA',
 'KAYLEE',
 'KIRA',
 'KYLIE',
 'LAILA',
 'LARA',
 'LAURA',
 'LAUREN',
 'LAYLA',
 'LEA',
 'LEAH',
 'LEILA',
 'LENA',
 'LEORA',
 'LIA',
 'LIANA',
 'LIBA',
 'LIBBY',
 'LILA',
 'LILAH',
 'LILIANA',
 'LILLIAN',
 'LILLY',
 'LILY',
 'LINA',
 'LOLA',
 'LONDON',
 'Jariel',
 'LUCY',
 'LYLA',
 'MACKENZIE',
 'MADELEINE',
 'MADELINE',
 'MADELYN',
 'MADISON',
 'MAEVE',
 'MAKAYLA',
 'MALAK',
 'MALKA',
 'MALKY',
 'MARGARET',
 'MARIA',
 'MARIAM',
 'MARY',
 'MATILDA',
 'MAYA',
 'MELANIE',
 'MIA',
 'MICHAELA',
 'MICHAL',
 'MICHELLE',
 'MIKAYLA',
 'MILA',
 'MILENA',
 'MINDY',
 'MIRI',
 'MIRIAM',
 'MOLLY',
 'MORGAN',
 'NAOMI',
 'NATALIA',
 'NATALIE',
 'NECHAMA',
 'NICOLE',
 'NICOLETTE',
 'NINA',
 'NOA',
 'NORA',
 'OLIVIA',
 'PAIGE',
 'PARKER',
 'PEARL',
 'PENELOPE',
 'PEREL',
 'PESSY',
 'PHOEBE',
 'PIPER',
 'QUINN',
 'RACHEL',
 'RAIZEL',
 'RAIZY',
 'REBECCA',
 'REESE',
 'RIFKA',
 'RIFKY',
 'RILEY',
 'RIVKA',
 'RIVKY',
 'ROCHEL',
 'ROIZY',
 'ROSE',
 'RUBY',
 'RUCHY',
 'RUTH',
 'RYAN',
 'SABRINA',
 'SADIE',
 'SALMA',
 'SAMANTHA',
 'SARA',
 'SARAH',
 'SASHA',
 'SAVANNAH',
 'SCARLETT',
 'SERENA',
 'SHAINA',
 'SHAINDEL',
 'SHAINDY',
 'SHEVY',
 'SHIFRA',
 'SHIRA',
 'SHOSHANA',
 'SIENA',
 'SIENNA',
 'SIMA',
 'SIMI',
 'SIMONE',
 'SKYLAR',
 'SLOANE',
 'SOFIA',
 'SOPHIA',
 'SOPHIE',
 'STELLA',
 'SUMMER',
 'SURI',
 'SURY',
 'SYDNEY',
 'SYLVIA',
 'TALIA',
 'TAMAR',
 'TAYLOR',
 'TESSA',
 'TOBY',
 'TZIPORA',
 'TZIPORAH',
 'TZIPPY',
 'TZIVIA',
 'VALENTINA',
 'VALERIE',
 'VANESSA',
 'VERA',
 'VERONICA',
 'VERONIKA',
 'VICTORIA',
 'VIOLET',
 'VIVIAN',
 'VIVIENNE',
 'WILLA',
 'YACHET',
 'YAEL',
 'YASMINE',
 'YEHUDIS',
 'YIDES',
 'YITTY',
 'YOCHEVED',
 'ZISSY',
 'SCARLETT',
 'ZOEY',
 'AARAV',
 'AARON',
 'ABDUL',
 'ABDULLAH',
 'ADAM',
 'ADITYA',
 'ADRIAN',
 'AHMED',
 'AIDAN',
 'AIDEN',
 'ALAN',
 'ALEX',
 'ALEXANDER',
 'ALI',
 'ALLEN',
 'ALVIN',
 'ANDREW',
 'ANDY',
 'ANSON',
 'ANTHONY',
 'ARJUN',
 'ARMAAN',
 'ARYAN',
 'AUSTIN',
 'AYAAN',
 'AYDEN',
 'BENJAMIN',
 'BENSON',
 'BRANDON',
 'BRIAN',
 'BRYAN',
 'CALEB',
 'CALVIN',
 'CARSON',
 'CHARLES',
 'CHRISTIAN',
 'CHRISTOPHER',
 'CODY',
 'CONNOR',
 'DANIEL',
 'DANNY',
 'DARREN',
 'DAVID',
 'DEREK',
 'DEVIN',
 'DYLAN',
 'EASON',
 'EDISON',
 'EDWIN',
 'ELIJAH',
 'ELVIS',
 'ERIC',
 'ETHAN',
 'EVAN',
 'FARHAN',
 'FELIX',
 'GABRIEL',
 'GAVIN',
 'GEORGE',
 'HARRISON',
 'HAYDEN',
 'HENRY',
 'IAN',
 'IBRAHIM',
 'ISAAC',
 'ISHAAN',
 'IVAN',
 'JACK',
 'JACKSON',
 'JACKY',
 'JACOB',
 'JADEN',
 'JAKE',
 'JAMES',
 'JASON',
 'JAY',
 'JAYDEN',
 'JEFFREY',
 'JEREMY',
 'JERRY',
 'JIA',
 'JOHN',
 'JOHNNY',
 'JONATHAN',
 'JORDAN',
 'JOSEPH',
 'JOSHUA',
 'JULIAN',
 'JUSTIN',
 'KAI',
 'KEVIN',
 'KINGSLEY',
 'KYLE',
 'LAWRENCE',
 'LEO',
 'LEON',
 'LIAM',
 'LOGAN',
 'LOUIS',
 'LUCAS',
 'LUKE',
 'MARCUS',
 'MARTIN',
 'MASON',
 'MATTHEW',
 'MAX',
 'MICHAEL',
 'MILES',
 'MOHAMED',
 'MOHAMMAD',
 'MOHAMMED',
 'MUHAMMAD',
 'NATHAN',
 'NATHANIEL',
 'NELSON',
 'NICHOLAS',
 'NOAH',
 'OLIVER',
 'OSCAR',
 'OWEN',
 'PATRICK',
 'PETER',
 'RAYAN',
 'RAYMOND',
 'RICHARD',
 'RICKY',
 'ROHAN',
 'RYAN',
 'SAMUEL',
 'SEAN',
 'SEBASTIAN',
 'SHAWN',
 'SIMON',
 'STANLEY',
 'STEVEN',
 'SYED',
 'TENZIN',
 'TERRY',
 'THOMAS',
 'TIMOTHY',
 'TONY',
 'TRAVIS',
 'TYLER',
 'VICTOR',
 'VINCENT',
 'WILLIAM',
 'WILSON',
 'XAVIER',
 'ZACHARY',
 'ZAIN',
 'ZAYAN',
 'AARON',
 'ABDOUL',
 'ABDOULAYE',
 'ADAM',
 'ADEN',
 'ADONIS',
 'ADRIAN',
 'AHMED',
 'AIDAN',
 'AIDEN',
 'ALEXANDER',
 'ALI',
 'ALIJAH',
 'ALVIN',
 'AMADOU',
 "AMAR'E",
 'AMARE',
 'AMARI',
 'AMIR',
 'ANDRE',
 'ANDREW',
 'ANGEL',
 'ANTHONY',
 'ANTONIO',
 'ASHTON',
 'AUSTIN',
 'AVERY',
 'AYDEN',
 'BENJAMIN',
 'BLAKE',
 'BRANDON',
 'BRIAN',
 'BRYAN',
 'BRYCE',
 'BRYSON',
 'CALEB',
 'CAMERON',
 'CARMELO',
 'CARTER',
 'CAYDEN',
 'CHAD',
 'CHANCE',
 'CHARLES',
 'CHASE',
 'CHRIS',
 'CHRISTIAN',
 'CHRISTOPHER',
 'CODY',
 'COREY',
 'DANIEL',
 'DARIUS',
 'DARREN',
 'DAVID',
 'DERRICK',
 'DEVIN',
 'DEVON',
 'DOMINIC',
 'DONOVAN',
 'DWAYNE',
 'DYLAN',
 'EDWARD',
 'ELI',
 'ELIAS',
 'ELIJAH',
 'EMMANUEL',
 'ERIC',
 'ETHAN',
 'EVAN',
 'GABRIEL',
 'GAVIN',
 'GEORGE',
 'GIOVANNI',
 'HASSAN',
 'HAYDEN',
 'HUNTER',
 'IAN',
 'SERENA',
 'IBRAHIMA',
 'ISAAC',
 'ISAIAH',
 'ISHMAEL',
 'ISIAH',
 'JACE',
 'JACKSON',
 'JACOB',
 'JADEN',
 'JAHEIM',
 'JAHMIR',
 'JAIDEN',
 'JALEN',
 'JAMAL',
 'JAMEL',
 'JAMES',
 'JAMIR',
 'JARED',
 'JASIAH',
 'JASON',
 'JAYDEN',
 'JAYLEN',
 'JAYSON',
 'JELANI',
 'JEREMIAH',
 'JEREMY',
 'JERMAINE',
 'JESSE',
 'JOEL',
 'JOHN',
 'JONATHAN',
 'JORDAN',
 'JOSEPH',
 'JOSHUA',
 'JOSIAH',
 'SHAINA',
 'JUSTICE',
 'JUSTIN',
 'KADEN',
 'KAI',
 'KAIDEN',
 'KALEB',
 'KAMARI',
 'KAMERON',
 'KAYDEN',
 'KEITH',
 'KENNETH',
 'KEVIN',
 'KHALIL',
 'KING',
 'KIYAN',
 'KYLE',
 'KYMANI',
 'LAMAR',
 'LANDON',
 'LEVI',
 'LIAM',
 'LOGAN',
 'LUCAS',
 'MAKAI',
 'MALACHI',
 'MALCOLM',
 'MALIK',
 'MAMADOU',
 'MARC',
 'MARCUS',
 'MARQUIS',
 'MASON',
 'MATTHEW',
 'MAURICE',
 'MEKHI',
 'MESSIAH',
 'MICAH',
 'MICHAEL',
 'MILES',
 'MOHAMED',
 'MOHAMMED',
 'MOUSSA',
 'MYLES',
 'NANA',
 'NASIR',
 'NATHAN',
 'NATHANIEL',
 'NEHEMIAH',
 'NICHOLAS',
 'NICOLAS',
 'NIGEL',
 'NOAH',
 'OMAR',
 'OMARI',
 'OUSMANE',
 'PATRICK',
 'PRESTON',
 'PRINCE',
 'QUINCY',
 'RICARDO',
 'RICHARD',
 'ROBERT',
 'RODNEY',
 'RYAN',
 'SAMUEL',
 'SEAN',
 'SEBASTIAN',
 'SEKOU',
 'SETH',
 'SHAINDEL',
 'SINCERE',
 'STEPHEN',
 'STEVEN',
 'TERRELL',
 'TERRENCE',
 'TIMOTHY',
 'TRAVIS',
 'TRISTAN',
 'TROY',
 'TYLER',
 'VICTOR',
 'WILLIAM',
 'XAVIER',
 'ZACHARY',
 'ZAIRE',
 'ZION',
 'ZYAIRE',
 'AARON',
 'ABDIEL',
 'ABEL',
 'ABRAHAM',
 'ADAM',
 'ADEN',
 'ADONIS',
 'ADRIAN',
 'ADRIEL',
 'AIDAN',
 'AIDEN',
 'ALAN',
 'ALBERT',
 'ALBERTO',
 'ALDO',
 'ALEJANDRO',
 'ALEX',
 'ALEXANDER',
 'ALEXIS',
 'ALFREDO',
 'ALLAN',
 'ALLEN',
 'ALVIN',
 'AMIR',
 'ANDERSON',
 'ANDRE',
 'ANDRES',
 'ANDREW',
 'ANDY',
 'ANGEL',
 'ANGELO',
 'ANTHONY',
 
 'CHRISTY',
 'CINDY',
 'CLAIRE'

    ]
    options_html = ""
    for num in counts:
        options_html += f"<option value='{num}'>{num}</option>\n"
    return render_template('home.html' , child_names=child_names ,options_html=options_html) 

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        # Get form data
        year_of_birth = int(request.form['year_of_birth'])
        gender = request.form['gender']
        ethnicity = request.form['ethnicity']
        child_first_name = request.form['child_first_name']
        count = int(request.form['count'])
        
        # Create input data DataFrame
        input_data = {
            'year_of_birth': [year_of_birth],
            'gender': [gender],
            'ethnicity': [ethnicity],
            'child_first_name': [child_first_name],
            'count': [count]
        }
        input_df = pd.DataFrame(input_data)
        
        # Preprocess input data
        preprocessed_input_data = preprocessor.transform(input_df)
        
        # Make prediction
        prediction = model.predict(preprocessed_input_data)
        
        return render_template('result.html', prediction=prediction[0])

if __name__ == "__main__":
    app.run(debug=True)