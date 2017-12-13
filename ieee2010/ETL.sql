
create table `acemap-xyue1`.`IeeeAfter2014ToFieldOfStudy` as
select IeeeToMag.`PaperID`, PaperField.`FieldOfStudyIDMappedToKeyword`
from (
	select ieee2014.`PaperID`, `acemap-stage`.`IdId`.`MagPaperID`
	from `acemap-xyue1`.`IeeeAfter2014` ieee2014
	inner join `acemap-stage`.`IdId`
	on ieee2014.`PaperID` = `acemap-stage`.`IdId`.`PaperID`
) as IeeeToMag
inner join `mag-new-160205`.`PaperKeywords` PaperField
on IeeeToMag.`MagPaperID` = PaperField.`PaperID`;

create table `acemap-xyue1`.`IeeeAfter2014Reference` as
select ref.*
from `acemap-stage`.`ReferenceIEEE` ref
inner join `acemap-xyue1`.`IeeeAfter2014` ieee1
on ref.`CitingPaperID` = ieee1.`PaperID`
inner join `acemap-xyue1`.`IeeeAfter2014` ieee2
on ref.`CitedPaperID` = ieee2.`PaperID`;

create table `acemap-xyue1`.`IeeeAfter2014` as
select ieee2014.*
from (
	select *
	from `acemap-stage`.`RawDataIEEE`
	where Year >= 2014
) as ieee2014
inner join `acemap-stage`.`IdId`
on ieee2014.`PaperID` = `acemap-stage`.`IdId`.`PaperID`;

create table `acemap-xyue1`.`IeeeAfter2014ToFieldOfStudy` as
select IeeeToMag.`PaperID`, PaperField.`FieldOfStudyIDMappedToKeyword`
from `acemap-xyue1`.`IeeeAfter2014ToMag` IeeeToMag
inner join `mag-new-160205`.`PaperKeywords` PaperField
on IeeeToMag.`MagPaperID` = PaperField.`PaperID`;

inset into `acemap-xyue1`.`FieldOfStudyHierarchy`
select FieldsOfStudyID, 'L0', FieldsOfStudyID as pid, 'L0', 1.0
from (
	select distinct FieldsOfStudyID
	from `mag-new-160205`.`FieldsOfStudy`
	where FieldsOfStudyLevel = 'L0'
) as L0

select ieee.PaperID, f1.ParentFieldOfStudyID
from IeeeAfter2014ToFieldOfStudy ieee
inner join FieldOfStudyHierarchy f1
on ieee.FieldOfStudyIDMappedToKeyword = f1.ChildFieldOfStudyID

create table IeeeAfter2014ToMainField
select PaperID, field as Field, sum(score) as Score
from (
	select ieee.PaperID, f.ParentFieldOfStudyID as field, ieee.score * f.Confidence as score
	from (
		select ieee.PaperID, f.ParentFieldOfStudyID as field, ieee.score * f.Confidence as score
		from (
			select ieee.PaperID, f.ParentFieldOfStudyID as field, ieee.score * f.Confidence as score
			from (
				select ieee.PaperID, ieee.FieldOfStudyIDMappedToKeyword as field, 1.0 as score
				from IeeeAfter2014ToFieldOfStudy ieee
			) as ieee
			inner join FieldOfStudyHierarchy as f
			on ieee.field = f.ChildFieldOfStudyID
		) as ieee
		inner join FieldOfStudyHierarchy as f
		on ieee.field = f.ChildFieldOfStudyID
	) as ieee
	inner join FieldOfStudyHierarchy as f
	on ieee.field = f.ChildFieldOfStudyID
) as ieee
group by PaperID, field;

create table IeeeAfter2014ToMainFieldName as
select MF.PaperID, L0.FieldsOfStudyName, MF.Score
from (
	select distinct FieldsOfStudyID, FieldsOfStudyName
	from `mag-new-160205`.`FieldsOfStudy`
	where FieldsOfStudyLevel = 'L0'
) as L0
inner join IeeeAfter2014ToMainField as MF
on L0.FieldsOfStudy = MF.Field

create table `acemap-xyue1`.`IeeeAfter2014ToFieldOfStudy` as
select IeeeToMag.`PaperID`, PaperField.`FieldOfStudyIDMappedToKeyword`
from `acemap-xyue1`.`IeeeAfter2014ToMag` IeeeToMag
inner join `mag-new-160205`.`PaperKeywords` PaperField
on IeeeToMag.`MagPaperID` = PaperField.`PaperID`;

create table `acemap-xyue1`.`MagToFieldOfStudy` as
select IeeeToMag.`MagPaperID`, PaperField.`FieldOfStudyIDMappedToKeyword`
from `acemap-xyue1`.`Mag` IeeeToMag
inner join `mag-new-160205`.`PaperKeywords` PaperField
on IeeeToMag.`MagPaperID` = PaperField.`PaperID`;

select count(*) from MagToFieldOfStudy;
select count(*) from IeeeAfter2014ToFieldOfStudy;


select *
from `mag-new-160205`.`FieldsOfStudy`
where FieldsOfStudyLevel = 'L0';

select 1, FieldsOfStudyLevel, FieldsOfStudyId from `mag-new-160205`.`FieldsOfStudy`
where FieldsOfStudyLevel = 'L0';


insert into FieldOfStudyHierarchy
select FieldsOfStudyID, 'L0', FieldsOfStudyID as pid, 'L0', 1.0
from (
	select distinct FieldsOfStudyID
	from `mag-new-160205`.`FieldsOfStudy`
	where FieldsOfStudyLevel = 'L0'
) as L0;


create table IeeeAfter2014ToMainField
select PaperID, field as Field, sum(score) as Score
from (
	select ieee.PaperID, f.ParentFieldOfStudyID as field, (ieee.score * f.Confidence) as score
	from (
		select ieee.PaperID, f.ParentFieldOfStudyID as field, ieee.score * f.Confidence as score
		from (
			select ieee.PaperID, f.ParentFieldOfStudyID as field, ieee.score * f.Confidence as score
			from (
				select ieee.PaperID, ieee.FieldOfStudyIDMappedToKeyword as field, 1.0 as score
				from IeeeAfter2014ToFieldOfStudy ieee
			) as ieee
			inner join FieldOfStudyHierarchy as f
			on ieee.field = f.ChildFieldOfStudyID
		) as ieee
		inner join FieldOfStudyHierarchy as f
		on ieee.field = f.ChildFieldOfStudyID
	) as ieee
	inner join FieldOfStudyHierarchy as f
	on ieee.field = f.ChildFieldOfStudyID
) as ieee
group by PaperID, field;


create table IeeeAfter2014ToMainFieldName as
select MF.PaperID, L0.FieldsOfStudyName, MF.Score
from (
	select distinct FieldsOfStudyID, FieldsOfStudyName
	from `mag-new-160205`.`FieldsOfStudy`
	where FieldsOfStudyLevel = 'L0'
) as L0
inner join IeeeAfter2014ToMainField as MF
on L0.FieldsOfStudyID = MF.Field;

select count(*) from IeeeAfter2014ToFieldOfStudy;
select count(*) from IeeeAfter2014ToMainFieldName;

alter table IeeeAfter2014ToMainFieldName add index (PaperID);

create table IeeeAfter2014ToCatagory
SELECT a.PaperID, a.FieldsOfStudyName as Catagory
FROM IeeeAfter2014ToMainFieldName a
LEFT OUTER JOIN IeeeAfter2014ToMainFieldName b
ON a.PaperID = b.PaperID AND a.Score < b.Score
WHERE b.PaperID IS NULL;

RENAME TABLE IeeeAfter2014ToCatagory TO TMP1;
CREATE TABLE TMP2 LIKE TMP1;
ALTER TABLE TMP2 ADD primary key (PaperID);
INSERT IGNORE INTO TMP2 SELECT * FROM TMP1;
DROP TABLE TMP1;
RENAME TABLE TMP2 TO IeeeAfter2014ToCatagory;

select count(*) from IeeeAfter2014ToCatagory;
select count(*) from IeeeAfter2014;

rename table IeeeAfter2014 to tmp1;
create table IeeeAfter2014 like tmp1;
alter table IeeeAfter2014 add column Catagory varchar(500);
insert into IeeeAfter2014
select tmp1.*, cat.`Catagory`
from tmp1
inner join IeeeAfter2014ToCatagory as cat
on tmp1.`PaperID` = cat.`PaperID`;
drop table tmp1;

rename table IeeeAfter2014Reference to tmp1;
create table `acemap-xyue1`.`IeeeAfter2014Reference` like tmp1;
insert into IeeeAfter2014Reference
select ref.*
from tmp1 ref
inner join `acemap-xyue1`.`IeeeAfter2014` ieee1
on ref.`CitingPaperID` = ieee1.`PaperID`
inner join `acemap-xyue1`.`IeeeAfter2014` ieee2
on ref.`CitedPaperID` = ieee2.`PaperID`;

select count(*) from IeeeAfter2014Reference;
select count
