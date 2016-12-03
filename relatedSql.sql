
SELECT
	ad_id as ad_id,
	tags,
	titlev as titlev,
	type as region_type,
	status_id as status
FROM
(
	SELECT DISTINCT
		id as ad_id,
		tags,
		titlev,
		region_id,
		status_id
	FROM table_name_1  #obtain raw data from database
	WHERE created_date between '@start_date@' and '@end_date@'
) b
LEFT JOIN
(
	SELECT
		id,
		type
	FROM table_name_2    #obtain raw data from database
) c
on b.region_id = c.id

