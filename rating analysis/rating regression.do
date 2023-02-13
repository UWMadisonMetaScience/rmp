clear
import delimited "review_byfield.csv"

encode(school_name), gen(school_id)
encode(department_name), gen(dept_id)
encode(field), gen(field_id)

forvalues field = 1/8 {
	display `field'
	reghdfe student_star is_female student_difficult if field_id == `field', absorb(school_id post_year) vce(cluster id)
}

reghdfe student_star is_female student_difficult, absorb(school_id post_year field_id) vce(cluster id)