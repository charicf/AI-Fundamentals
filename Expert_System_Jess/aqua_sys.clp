(defglobal 	?*PH_MIN* = 6
    	   	?*PH_MAX* = 7
    		?*TEMPERATURE_MIN* = 18
    		?*TEMPERATURE_MAX* = 30
    		?*DISOLVED_OXYGEN_MIN* = 5
    		?*DISOLVED_OXYGEN_MAX* = 8
    	   	?*AMMONIA_MAX* = 1
    		?*NITRITE_MAX* = 1
    		?*NITRATE_MIN* = 5
		    ?*NITRATE_MAX* = 150
		    ?*CARBONATE_HARDNESS_MIN* = 60
		    ?*CARBONATE_HARDNESS_MAX* = 140)

(deftemplate water_quality
    "A patient whose biochemical blood test will be analyzed"
    (slot ph) ;id of the patient
    (slot temperature) ;sex of the patient 'M' or 'F'
    (slot disolved_oxygen) ;the age of the patient
    (slot ammonia)
    (slot nitrite)
    (slot nitrate)
    (slot carbonate_hardness)
    )

(deftemplate measure
    (slot name) ; Name of measure
    (slot value) ; Value of measure
    (slot units)) ; Units of measure

(deftemplate measure_analysis
    (slot name) ; Name of characteristic
    (slot value)) ; Result of analysis

;functions to determine wheter the value of a test is High Normal or Low
(deffunction determine_level (?value ?min ?max)
    (printout t ?value crlf)
    (if (> ?value ?max) then
          (return H)
       else (if (< ?value ?min) then
          (return L)
            else (return N)))
)

(deffunction print_msg (?message)
    (printout t ?message crlf))

(deffunction is_a_number (?value)
 "Return TRUE if ?value is a number"
 	(if (integerp ?value) then
        ;(printout t "its  an integer" crlf)
 		(return TRUE)
 	else
        (printout t "Wrong type of answer, please try again" crlf)
 		(return FALSE)))

;check the type of the required value
(deffunction is_of_type (?answer ?type ?valid)
    (if (eq ?answer "") then (return FALSE))
 "Check that the answer has the right form"
 (if (eq ?type multi) then
 	(foreach ?item ?valid
 		(if (eq (sym-cat ?answer) (sym-cat ?item)) then
 		(return TRUE)))
 	(return FALSE))
 (if (eq ?type number) then
 (return (is_a_number ?answer))))

;code from the book jess in action to read input data
(deffunction ask_user (?question ?type ?valid)
 "Ask a question, and return the answer"
 (bind ?answer "")
 ;(printout t (is_of_type ?answer ?type ?valid) crlf)
 (while (not (is_of_type ?answer ?type ?valid)) do
 	(printout t ?question " ")
 		(if (eq ?type multi) then
 			(printout t crlf "Valid answers are ")
 			(foreach ?item ?valid
 				(printout t ?item " "))
 		(printout t ":"))
 	(bind ?answer (read))
 )
 (return ?answer))
    
 ;; plain text
 ;(return (> (str-length ?answer) 0)))


(reset)

;(assert (measure (name PH) (value 4)))

;when ph values are needed
/*(defrule need_ph
    "Activated when ph test is needed"
    ;(declare (auto-focus TRUE))
    ;(MAIN::need-measure (name PH) (value ?ph_value))
    ;(MAIN::need-analysis (test-code CHCM) (value ?chcm-value))
    ;(not (measure (name PH)))
    (measure (name PH) (value nil))
    =>
    (print_msg "pH measure is necessary to continue with the examination.")
    (printout t "Reference 1 (" ?*PH_MIN* "-" ?*PH_MAX* ")" crlf)
    (bind ?value (ask_user "What is the PH value?" text nil))
    (assert (measure (name PH) (value ?value)))
    )

(watch all)
 /*(defrule wrong-rule
    ;(test(eq 1 1))
    (eq 1 1)
 	=>
 	(printout t "Just as I thought, 1 == 1!" crlf)) */
;(watch all)
(print_msg "Welcome to the control system for Aquaponics system. We need some initial values to assess the functioning of the system")

(bind ?value (ask_user "What is the pH of the water? (numeric value)" number nil))
(assert (measure (name PH) (value ?value)))

(bind ?value (ask_user "What is the temperature of the water? (numeric value)" number nil))
(assert (measure (name TEMP) (value ?value)))

(bind ?value (ask_user "What is the nitrate value of the water? (numeric value)" number nil))
(assert (measure (name NITRA) (value ?value)))

(bind ?value (ask_user "What is the carbonate hardness value of the water? (numeric value)" number nil))
(assert (measure (name KH) (value ?value)))


/*(defrule check_ph
    "Check the values of PH, TEMP, DO and KH"
    (measure (name PH) (value ?value))
     =>
    (printout t ?value crlf)
    (bind ?ph_result (determine_level ?value ?*PH_MIN* ?*PH_MAX*))
    (assert (measure_analysis (name PH) (value ?ph_result)))
    )*/

;check initial measures
(defrule check_initial_measures
    "Check the values of PH, TEMP, DO and KH"
    (measure (name PH) (value ?ph_value))
    (measure (name TEMP) (value ?temp_value))
    (measure (name NITRA) (value ?nitra_value))
    (measure (name KH) (value ?kh_value))
    =>
    (bind ?ph_result (determine_level ?ph_value ?*PH_MIN* ?*PH_MAX*))
    (bind ?temp_result (determine_level ?temp_value ?*TEMPERATURE_MIN* ?*TEMPERATURE_MAX*))
    (bind ?nitra_result (determine_level ?nitra_value ?*NITRATE_MIN* ?*NITRATE_MAX*))
    (bind ?kh_result (determine_level ?kh_value ?*CARBONATE_HARDNESS_MIN* ?*CARBONATE_HARDNESS_MAX*))

    (assert (measure_analysis (name PH) (value ?ph_result)))
    (assert (measure_analysis (name TEMP) (value ?temp_result)))
    (assert (measure_analysis (name NITRA) (value ?nitra_result)))
    (assert (measure_analysis (name KH) (value ?kh_result)))
    )

(defrule balanced_system
    (measure_analysis (name PH) (value N))
    (measure_analysis (name TEMP) (value N))
    (measure_analysis (name NITRA) (value N))
    (measure_analysis (name KH) (value N))
    =>
    (printout t "The system is balanced. Tests should be done daily" crlf)
    )

(defrule unbalanced_system
    (measure_analysis (name PH) (value L|H))
    (measure_analysis (name TEMP) (value L|H))
    (measure_analysis (name NITRA) (value L|H))
    (measure_analysis (name KH) (value L|H))
    =>
    (printout t "The system is completely unbalanced. It requires a deep analysis and hard work" crlf)
    )

(defrule high_temp_only
    (measure_analysis (name PH) (value N))
    (measure_analysis (name TEMP) (value H))
    (measure_analysis (name NITRA) (value N))
    (measure_analysis (name KH) (value N|H))
    =>
    (printout t "Temperature is High. It might cause a low disolved Oxygen in water." crlf)
    (bind ?value (ask_user "What is the disolved Oxygen of the water? (numeric value)" number nil))
	(assert (measure (name DO) (value ?value)))
    )

(defrule high_ph_only
    (measure_analysis (name PH) (value H))
    (measure_analysis (name TEMP) (value N))
    (measure_analysis (name NITRA) (value N))
    (measure_analysis (name KH) (value L|N|H))
    (measure (name PH) (value ?value&:(> ?value 7.5)))
    =>
    (printout t "pH is High. PH is very important for balance, it must be fixed." crlf)
    (printout t " Nutrient deficiencies of iron, phosphorus and manganese for plants and toxic 
        for fish (affects the toxicity of ammonia to fish)" crlf)
    )

(defrule low_ph_only
    (measure_analysis (name PH) (value L))
    (measure_analysis (name TEMP) (value N))
    (measure_analysis (name NITRA) (value N))
    (measure_analysis (name KH) (value N|H))
    =>
    (printout t "pH is Low. PH is very important for balance, it must be fixed." crlf)
    (printout t " Bacteria’s capacity to convert ammonia into nitrate will reduce" crlf)

    )

(defrule high_temp_ph
    (measure_analysis (name PH) (value H))
    (measure_analysis (name TEMP) (value H))
    (measure_analysis (name NITRA) (value L|N))
    (measure_analysis (name KH) (value L|N|H))
    =>
    (printout t "System is out f balance. Ammonia and nitrites levels should be checked" crlf)
    (bind ?value (ask_user "What is the ammoniac of the water? (numeric value)" number nil))
	(assert (measure (name AMM) (value ?value)))
    (bind ?value (ask_user "What are the nitrites of the water? (numeric value)" number nil))
	(assert (measure (name NITRI) (value ?value)))
    )

(defrule high_nitra
    (measure_analysis (name PH) (value N))
    (measure_analysis (name TEMP) (value N))
    (measure_analysis (name NITRA) (value H))
    (measure_analysis (name KH) (value N|H))
    =>
    (printout t "System is functioning correctly. However, nitrates are high so it is
        advisible to change the water." crlf)
    )

(defrule high_nitra_2
    (measure_analysis (name PH) (value N))
    (measure_analysis (name TEMP) (value N))
    (measure_analysis (name NITRA) (value H))
    (measure_analysis (name KH) (value N|H))
    (measure (name DO) (value ?value&:(> ?value 250)))
    =>
    (printout t "Nitrates are high. It may have effect on plants, excessive vegetative growth and 
        hazardous accumulation of nitrates in leaves, which is dangerous for human health" crlf)
    )

(defrule high_nitra_3
    (measure_analysis (name PH) (value N))
    (measure_analysis (name TEMP) (value N))
    (measure_analysis (name NITRA) (value H))
    (measure_analysis (name KH) (value N|H))
    (measure (name DO) (value ?value&:(> ?value 300)))
    =>
    (printout t "Nitrates are high. It will also have negative effects on fishes" crlf)
    )

(defrule low_KH
    (measure_analysis (name PH) (value N))
    (measure_analysis (name TEMP) (value N))
    (measure_analysis (name NITRA) (value N))
    (measure_analysis (name KH) (value L))
    =>
    (printout t "Carbonate hardness (KH) is low so there is a risk that pH changes drastically. 
        KH should be increased" crlf)
    )

(defrule check_secondary_measures
    (measure (name AMM) (value ?amm_value))
    (measure (name NITRI) (value ?nitri_value))
    =>
    (bind ?amm_result (determine_level ?amm_value 0 ?*AMMONIA_MAX*))
    (bind ?nitri_result (determine_level ?nitri_value 0 ?*NITRITE_MAX*))
    (assert (measure_analysis (name AMM) (value ?amm_result)))
    (assert (measure_analysis (name NITRI) (value ?nitri_result)))
    )

(defrule high_amm_nitri
    (measure_analysis (name AMM) (value H))
    (measure_analysis (name NITRI) (value H))
    =>
    (printout t "High levels of ammonia and nitrites are toxic for fishes. Prolonged exposure will 
        cause damage to the fishes’ central nervous system and gills, resulting in loss of 
        equilibrium, impaired respiration and convulsions" crlf)
    (printout t "Temperature and pH must be decreased " crlf)
    )

(defrule high_amm
    (measure_analysis (name AMM) (value H))
    (measure_analysis (name NITRI) (value L|N|H))
    =>
    (printout t "High levels of ammonia is toxic for fishes. Prolonged exposure will 
        cause damage to the fishes’ central nervous system and gills, resulting in loss of 
        equilibrium, impaired respiration and convulsions" crlf)
    (printout t "Temperature and pH must be decreased " crlf)
    )

(defrule high_nitri
    (measure_analysis (name AMM) (value L|N|H))
    (measure_analysis (name NITRI) (value H))
    =>
    (printout t "High levels of nitrites are toxic for fishes. Prolonged exposure will 
        cause damage to the fishes’ central nervous system and gills, resulting in loss of 
        equilibrium, impaired respiration and convulsions" crlf)
    (printout t "Temperature and pH must be decreased " crlf)
    )

(defrule critical_high_amm
    (measure_analysis (name AMM) (value H))
    (measure (name AMM) (value ?value&:(> ?value 4)))
    =>
    (printout t "Exponentially deteriorating situation: biofilter is overwhelmed by ammonia, 
        which causes bacteria to die and the ammonia increases even more. Must be fixed" crlf)
    )

(defrule normal_amm_nitri
    (measure_analysis (name AMM) (value N|L))
    (measure_analysis (name NITRI) (value N|L))
    =>
    (printout t "Levels of ammonia and nitrites are ok." crlf)
    (printout t "Temperature and pH must be decreased" crlf)
    )

(defrule check_DO
    (measure (name DO) (value ?do_value))
    =>
    (bind ?do_result (determine_level ?do_value ?*DISOLVED_OXYGEN_MIN* ?*DISOLVED_OXYGEN_MAX*))
    (assert (measure_analysis (name DO) (value ?do_result)))
    )

(defrule low_DO
    (measure_analysis (name DO) (value L))
    (measure (name DO) (value ?value&:(>= ?value 2)))
    =>
    (printout t "Low disolved Oxygen in water is toxic for fish and causes low absortion of 
        nutriens by plants" crlf)
    (printout t "It is recommended that aeration be increased using air pumps in warm locations or
during the hottest times of the year, especially if raising delicate fish." crlf)
    )

(defrule critical_low_DO
    (measure_analysis (name DO) (value L))
    (measure (name DO) (value ?value&:(< ?value 2)))
    =>
    (printout t "WARNING: critical low levels of DO. Nitrification will stop. Increase aeration prontly" crlf)
    )

/*(defrule not_implemented
    (declare (salience -100))
    =>
    (printout t "This case is not implemented yet" crlf))*/
;(reset)
(run)