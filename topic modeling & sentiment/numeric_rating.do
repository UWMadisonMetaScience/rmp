*** 1-rating topics*** 

clear
//import delimited "tf_prob_stata_1.csv"

// encode(field), gen(field_id)
// gen is_female = 0
// replace is_female = 1 if gender == "female"

use "tf_prob_stata_1.dta"

mean topic_0-topic_89

forvalues t = 0/89 {
	display `t'
	reghdfe topic_`t' is_female, absorb(post_year field_id school_id) vce(cluster id)
	est sto m`t'
}
outreg2 [m0 m1 m2 m3 m4 m5 m6 m7 m8 m9 m10 m11 m12 m13 m14 m15 m16 m17 m18 m19 m20 m21 m22 m23 m24 m25 m26 m27 m28 m29 m30 m31 m32 m33 m34 m35 m36 m37 m38 m39 m40 m41 m42 m43 m44 m45 m46 m47 m48 m49 m50 m51 m52 m53 m54 m55 m56 m57 m58 m59 m60 m61 m62 m63 m64 m65 m66 m67 m68 m69 m70 m71 m72 m73 m74 m75 m76 m77 m78 m79 m80 m81 m82 m83 m84 m85 m86 m87 m88 m89] using "prob_1.xls", append stats(coef pval ci_low ci_high) stnum(replace coef=coef*100, replace ci_low=ci_low*100, replace ci_high=ci_high*100) noaster noparen nocons dec(3) excel label

// replace space with underline
gen field_nospace = field
replace field_nospace = "Applied_Sciences" if field == "Applied Sciences"
replace field_nospace = "Natural_Sciences" if field == "Natural Sciences"
replace field_nospace = "Math_Computing" if field == "Math & Computing"
replace field_nospace = "Medicine_Health" if field == "Medicine Health"
replace field_nospace = "Social_Sciences" if field == "Social Sciences"

global fields "Applied_Sciences Natural_Sciences Math_Computing Engineering Medicine_Health Social_Sciences Education Humanities" //

foreach f of global fields {
	forvalues t = 0/89 {
		display "`f'"
		display `t'
		reghdfe topic_`t' is_female if field_nospace == "`f'", absorb(post_year school_id) vce(cluster id)
		est sto `f'`t'
	}
	outreg2 [`f'0 `f'1 `f'2 `f'3 `f'4 `f'5 `f'6 `f'7 `f'8 `f'9 `f'10 `f'11 `f'12 `f'13 `f'14 `f'15 `f'16 `f'17 `f'18 `f'19 `f'20 `f'21 `f'22 `f'23 `f'24 `f'25 `f'26 `f'27 `f'28 `f'29 `f'30 `f'31 `f'32 `f'33 `f'34 `f'35 `f'36 `f'37 `f'38 `f'39 `f'40 `f'41 `f'42 `f'43 `f'44 `f'45 `f'46 `f'47 `f'48 `f'49 `f'50 `f'51 `f'52 `f'53 `f'54 `f'55 `f'56 `f'57 `f'58 `f'59 `f'60 `f'61 `f'62 `f'63 `f'64 `f'65 `f'66 `f'67 `f'68 `f'69 `f'70 `f'71 `f'72 `f'73 `f'74 `f'75 `f'76 `f'77 `f'78 `f'79 `f'80 `f'81 `f'82 `f'83 `f'84 `f'85 `f'86 `f'87 `f'88 `f'89] using "prob_1_`f'.xls", append stats(coef pval ci_low ci_high) stnum(replace coef=coef*100, replace ci_low=ci_low*100, replace ci_high=ci_high*100) noaster noparen nocons dec(3) excel label
}

*** 1-rating sentiment ***
// overall
reghdfe pos is_female, absorb(post_year field_id school_id) vce(cluster id)
reghdfe neg is_female, absorb(post_year field_id school_id) vce(cluster id)

forvalues t = 0/89 {
	display `t'
	reghdfe neg is_female [pweight=topic_`t'], absorb(post_year field_id school_id) vce(cluster id)
	est sto s`t'
}
outreg2 [s0 s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 s13 s14 s15 s16 s17 s18 s19 s20 s21 s22 s23 s24 s25 s26 s27 s28 s29 s30 s31 s32 s33 s34 s35 s36 s37 s38 s39 s40 s41 s42 s43 s44 s45 s46 s47 s48 s49 s50 s51 s52 s53 s54 s55 s56 s57 s58 s59 s60 s61 s62 s63 s64 s65 s66 s67 s68 s69 s70 s71 s72 s73 s74 s75 s76 s77 s78 s79 s80 s81 s82 s83 s84 s85 s86 s87 s88 s89] using "sentiment_1.xls", append stats(coef pval ci_low ci_high) noaster noparen nocons dec(3) excel label

foreach f of global fields {
	forvalues t = 0/89 {
		reghdfe neg is_female [pweight=topic_`t']  if field_nospace == "`f'", absorb(post_year school_id) vce(cluster id)
		est sto s`f'`t'
	}
	outreg2 [s`f'0 s`f'1 s`f'2 s`f'3 s`f'4 s`f'5 s`f'6 s`f'7 s`f'8 s`f'9 s`f'10 s`f'11 s`f'12 s`f'13 s`f'14 s`f'15 s`f'16 s`f'17 s`f'18 s`f'19 s`f'20 s`f'21 s`f'22 s`f'23 s`f'24 s`f'25 s`f'26 s`f'27 s`f'28 s`f'29 s`f'30 s`f'31 s`f'32 s`f'33 s`f'34 s`f'35 s`f'36 s`f'37 s`f'38 s`f'39 s`f'40 s`f'41 s`f'42 s`f'43 s`f'44 s`f'45 s`f'46 s`f'47 s`f'48 s`f'49 s`f'50 s`f'51 s`f'52 s`f'53 s`f'54 s`f'55 s`f'56 s`f'57 s`f'58 s`f'59 s`f'60 s`f'61 s`f'62 s`f'63 s`f'64 s`f'65 s`f'66 s`f'67 s`f'68 s`f'69 s`f'70 s`f'71 s`f'72 s`f'73 s`f'74 s`f'75 s`f'76 s`f'77 s`f'78 s`f'79 s`f'80 s`f'81 s`f'82 s`f'83 s`f'84 s`f'85 s`f'86 s`f'87 s`f'88 s`f'89] using "sentiment_1_`f'.xls", append stats(coef pval ci_low ci_high) stnum(replace coef=coef*100, replace ci_low=ci_low*100, replace ci_high=ci_high*100) noaster noparen nocons dec(3) excel label
}

*** 5-rating topics*** 
clear
use "tf_prob_stata_5.dta"

mean topic_0-topic_72

forvalues t = 0/72 {
	display `t'
	reghdfe topic_`t' is_female, absorb(post_year field_id school_id) vce(cluster id)
	est sto m`t'
}
outreg2 [m0 m1 m2 m3 m4 m5 m6 m7 m8 m9 m10 m11 m12 m13 m14 m15 m16 m17 m18 m19 m20 m21 m22 m23 m24 m25 m26 m27 m28 m29 m30 m31 m32 m33 m34 m35 m36 m37 m38 m39 m40 m41 m42 m43 m44 m45 m46 m47 m48 m49 m50 m51 m52 m53 m54 m55 m56 m57 m58 m59 m60 m61 m62 m63 m64 m65 m66 m67 m68 m69 m70 m71 m72] using "prob_5.xls", append stats(coef pval ci_low ci_high) stnum(replace coef=coef*100, replace ci_low=ci_low*100, replace ci_high=ci_high*100) noaster noparen nocons dec(3) excel label

// replace space with underline
gen field_nospace = field
replace field_nospace = "Applied_Sciences" if field == "Applied Sciences"
replace field_nospace = "Natural_Sciences" if field == "Natural Sciences"
replace field_nospace = "Math_Computing" if field == "Math & Computing"
replace field_nospace = "Medicine_Health" if field == "Medicine Health"
replace field_nospace = "Social_Sciences" if field == "Social Sciences"

global fields "Education Humanities" //  Applied_Sciences Natural_Sciences Math_Computing Engineering Medicine_Health Social_Sciences

foreach f of global fields {
	forvalues t = 0/72 {
		display "`f'"
		display `t'
		reghdfe topic_`t' is_female if field_nospace == "`f'", absorb(post_year school_id) vce(cluster id)
		est sto `f'`t'
	}
	outreg2 [`f'0 `f'1 `f'2 `f'3 `f'4 `f'5 `f'6 `f'7 `f'8 `f'9 `f'10 `f'11 `f'12 `f'13 `f'14 `f'15 `f'16 `f'17 `f'18 `f'19 `f'20 `f'21 `f'22 `f'23 `f'24 `f'25 `f'26 `f'27 `f'28 `f'29 `f'30 `f'31 `f'32 `f'33 `f'34 `f'35 `f'36 `f'37 `f'38 `f'39 `f'40 `f'41 `f'42 `f'43 `f'44 `f'45 `f'46 `f'47 `f'48 `f'49 `f'50 `f'51 `f'52 `f'53 `f'54 `f'55 `f'56 `f'57 `f'58 `f'59 `f'60 `f'61 `f'62 `f'63 `f'64 `f'65 `f'66 `f'67 `f'68 `f'69 `f'70 `f'71 `f'72] using "prob_5_`f'.xls", append stats(coef pval ci_low ci_high) stnum(replace coef=coef*100, replace ci_low=ci_low*100, replace ci_high=ci_high*100) noaster noparen nocons dec(3) excel label
}

*** 5-rating sentiment*** 
reghdfe pos is_female, absorb(post_year field_id school_id) vce(cluster id)
reghdfe neg is_female, absorb(post_year field_id school_id) vce(cluster id)

forvalues t = 0/72 {
	display `t'
	reghdfe pos is_female [pweight=topic_`t'], absorb(post_year field_id school_id) vce(cluster id)
	est sto s`t'
}
outreg2 [s0 s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 s13 s14 s15 s16 s17 s18 s19 s20 s21 s22 s23 s24 s25 s26 s27 s28 s29 s30 s31 s32 s33 s34 s35 s36 s37 s38 s39 s40 s41 s42 s43 s44 s45 s46 s47 s48 s49 s50 s51 s52 s53 s54 s55 s56 s57 s58 s59 s60 s61 s62 s63 s64 s65 s66 s67 s68 s69 s70 s71 s72] using "sentiment_5.xls", append stats(coef pval ci_low ci_high) noaster noparen nocons dec(3) excel label

foreach f of global fields {
	forvalues t = 0/72 {
		display `t'
		reghdfe pos is_female [pweight=topic_`t'] if field_nospace == "`f'", absorb(post_year school_id) vce(cluster id)
		est sto s`f'`t'
	}
	outreg2 [s`f'0 s`f'1 s`f'2 s`f'3 s`f'4 s`f'5 s`f'6 s`f'7 s`f'8 s`f'9 s`f'10 s`f'11 s`f'12 s`f'13 s`f'14 s`f'15 s`f'16 s`f'17 s`f'18 s`f'19 s`f'20 s`f'21 s`f'22 s`f'23 s`f'24 s`f'25 s`f'26 s`f'27 s`f'28 s`f'29 s`f'30 s`f'31 s`f'32 s`f'33 s`f'34 s`f'35 s`f'36 s`f'37 s`f'38 s`f'39 s`f'40 s`f'41 s`f'42 s`f'43 s`f'44 s`f'45 s`f'46 s`f'47 s`f'48 s`f'49 s`f'50 s`f'51 s`f'52 s`f'53 s`f'54 s`f'55 s`f'56 s`f'57 s`f'58 s`f'59 s`f'60 s`f'61 s`f'62 s`f'63 s`f'64 s`f'65 s`f'66 s`f'67 s`f'68 s`f'69 s`f'70 s`f'71 s`f'72 ] using "sentiment_5_`f'.xls", append stats(coef pval ci_low ci_high) stnum(replace coef=coef*100, replace ci_low=ci_low*100, replace ci_high=ci_high*100) noaster noparen nocons dec(3) excel label
}