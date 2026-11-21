## 1. Extraction table

| number | logline | twist_type | hero_role_group | setting_group | cliffhanger_type | city | hero_job | villain | secret | evidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A Seattle valet secretly owns the garage her father is about to lose. At the auction the clerk reads her name off the deed. | hidden_identity | service_worker | us_city_named | reveal | Seattle | valet | unknown | valet owns garage | secretly owns the garage |
| 2 | A Seattle waitress keeps her ownership of the diner from her sister, who wants to sell it. At closing the buyer turns the license around and points to the waitress's name. | hidden_identity | service_worker | us_city_named | reveal | Seattle | waitress | unknown | waitress owns diner | keeps her ownership of the diner |
| 3 | A Chicago cleaner hides the fact that she owns the motel where her brother pockets the rent. He opens the tax bill and sees her name. | hidden_identity | service_worker | us_city_named | reveal | Chicago | cleaner | brother | cleaner owns motel | hides the fact that she owns |
| 4 | A student discovers her roommate has been auditioning under her name. The roommate gives her until curtain up to surrender the part or lose their apartment. | imposter_takes_place | student | unknown | choice_ultimatum | unknown | unknown | roommate | roommate took student's identity | auditioning under her name |
| 5 | A small-town surgeon comes home to expose the doctor who switched her patient's charts. He holds the surviving chart over a flame. | revenge_return | legal_medical | small_town | threat | unknown | surgeon | doctor | doctor switched charts | comes home to expose the doctor |
| 6 | A violinist discovers her duet partner sold their only recording to pay his debts. The buyer knocks before she can confront him. | betrayal_by_ally | creative_artist | unknown | arrival | unknown | violinist | duet partner | partner sold recording | duet partner sold their only recording |

## 2. Distributions

### twist_type (6 known)

| Value | Count | Share | Mark |
| --- | --- | --- | --- |
| hidden_identity | 3 | 50.0% | FLAG |
| imposter_takes_place | 1 | 16.7% |  |
| revenge_return | 1 | 16.7% |  |
| betrayal_by_ally | 1 | 16.7% |  |
| unknown | 0 | excluded |  |

### hero_role_group (6 known)

| Value | Count | Share | Mark |
| --- | --- | --- | --- |
| service_worker | 3 | 50.0% | FLAG |
| student | 1 | 16.7% |  |
| legal_medical | 1 | 16.7% |  |
| creative_artist | 1 | 16.7% |  |
| unknown | 0 | excluded |  |

### setting_group (4 known)

| Value | Count | Share | Mark |
| --- | --- | --- | --- |
| us_city_named | 3 | 75.0% | FLAG |
| small_town | 1 | 25.0% |  |
| unknown | 2 | excluded |  |

### cliffhanger_type (6 known)

| Value | Count | Share | Mark |
| --- | --- | --- | --- |
| reveal | 3 | 50.0% | FLAG |
| choice_ultimatum | 1 | 16.7% |  |
| threat | 1 | 16.7% |  |
| arrival | 1 | 16.7% |  |
| unknown | 0 | excluded |  |

### city (3 known)

| Value | Count | Share | Mark |
| --- | --- | --- | --- |
| Seattle | 2 | 66.7% | FLAG |
| Chicago | 1 | 33.3% | FLAG |
| unknown | 3 | excluded |  |

## 3. Sameness Score

Modal pair: hidden_identity × service_worker. Matching rows: 1, 2, 3. **3/6 = 50.0%**.

## 4. Exposition check

Not applicable, loglines only.

## 5. Fix suggestions

### Logline 1

| field | changed_to | new_logline | why_fresh |
| --- | --- | --- | --- |
| cliffhanger_type | arrival | A Seattle valet secretly owns the garage her father is about to lose. Before bidding opens, her father walks in carrying his old garage keys. | Her father arrives before the sale begins. |
| cliffhanger_type | threat | A Seattle valet secretly owns the garage her father is about to lose. The auctioneer reaches for the gavel while her father is still parking outside. | The gavel sets a deadline for intervention. |
| cliffhanger_type | choice_ultimatum | A Seattle valet secretly owns the garage her father is about to lose. The clerk gives her ten seconds to show the deed or let the sale proceed. | Stopping the sale would expose her ownership. |

### Logline 2

| field | changed_to | new_logline | why_fresh |
| --- | --- | --- | --- |
| cliffhanger_type | arrival | A Seattle waitress keeps her ownership of the diner from her sister, who wants to sell it. Before the buyer can sign, their mother walks in carrying the diner's first menu. | A family witness interrupts the sale. |
| cliffhanger_type | threat | A Seattle waitress keeps her ownership of the diner from her sister, who wants to sell it. The buyer promises to strip the kitchen tonight unless someone challenges the sale. | The kitchen faces an immediate threat. |
| cliffhanger_type | choice_ultimatum | A Seattle waitress keeps her ownership of the diner from her sister, who wants to sell it. The buyer gives her until closing to sign away the diner or send her sister home empty-handed. | She must weigh ownership against her sister's plans. |

### Logline 3

| field | changed_to | new_logline | why_fresh |
| --- | --- | --- | --- |
| cliffhanger_type | arrival | A Chicago cleaner hides the fact that she owns the motel where her brother pockets the rent. They are counting the cash when a tenant arrives with a second rent receipt. | A tenant interrupts the private dispute. |
| cliffhanger_type | threat | A Chicago cleaner hides the fact that she owns the motel where her brother pockets the rent. He holds the only rent ledger over a lit burner. | The evidence is seconds from destruction. |
| cliffhanger_type | choice_ultimatum | A Chicago cleaner hides the fact that she owns the motel where her brother pockets the rent. To recover the missing rent she must sign a complaint as owner before her brother leaves town. | Recovering the money could expose her identity. |

## 6. Self-check

- #1 Ownership is explicit; the reason for the auction is unstated.
- #2 The sister could be acting in good faith.
- #4 Curtain up sets a deadline but leaves the scene location open.

- A small slate can cross the threshold after one edit.
- A shared trope can serve different emotional conflicts.
- Missing cities inflate shares among known cities.

## 7. CSV

```csv
number,logline,twist_type,hero_role_group,setting_group,cliffhanger_type,city,hero_job,villain,secret,evidence
1,A Seattle valet secretly owns the garage her father is about to lose. At the auction the clerk reads her name off the deed.,hidden_identity,service_worker,us_city_named,reveal,Seattle,valet,unknown,valet owns garage,secretly owns the garage
2,"A Seattle waitress keeps her ownership of the diner from her sister, who wants to sell it. At closing the buyer turns the license around and points to the waitress's name.",hidden_identity,service_worker,us_city_named,reveal,Seattle,waitress,unknown,waitress owns diner,keeps her ownership of the diner
3,A Chicago cleaner hides the fact that she owns the motel where her brother pockets the rent. He opens the tax bill and sees her name.,hidden_identity,service_worker,us_city_named,reveal,Chicago,cleaner,brother,cleaner owns motel,hides the fact that she owns
4,A student discovers her roommate has been auditioning under her name. The roommate gives her until curtain up to surrender the part or lose their apartment.,imposter_takes_place,student,unknown,choice_ultimatum,unknown,unknown,roommate,roommate took student's identity,auditioning under her name
5,A small-town surgeon comes home to expose the doctor who switched her patient's charts. He holds the surviving chart over a flame.,revenge_return,legal_medical,small_town,threat,unknown,surgeon,doctor,doctor switched charts,comes home to expose the doctor
6,A violinist discovers her duet partner sold their only recording to pay his debts. The buyer knocks before she can confront him.,betrayal_by_ally,creative_artist,unknown,arrival,unknown,violinist,duet partner,partner sold recording,duet partner sold their only recording
```
