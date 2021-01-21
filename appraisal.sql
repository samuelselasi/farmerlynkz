--
-- PostgreSQL database dump
--

-- Dumped from database version 12.5 (Ubuntu 12.5-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.5 (Ubuntu 12.5-0ubuntu0.20.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: gender_type; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.gender_type AS ENUM (
    'male',
    'female'
);


--
-- Name: role_type; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.role_type AS ENUM (
    'Director',
    'Admin',
    'Normal'
);


--
-- Name: annual_appraisal(integer, character varying, character varying, integer, character varying, integer, date, date); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.annual_appraisal(stdgrade integer, stdcomment character varying, stdfield character varying, stdappraisalid integer, stdstatus character varying, stdid integer, stddatestart date, stddateend date) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.annual_appraisal(Grade,Comment,Field,AppraisalID,Status,ID,DateStart,DateEnd)
values(stdGrade ,stdComment ,stdField,stdAppraisalID,stdStatus,stdID,stdDateStart,stdDateEnd);
return 'inserted successfully';
	   end;
$$;


--
-- Name: annual_plan(character varying, character varying, character varying, integer, integer, integer, character varying, date, date); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.annual_plan(stdresultareas character varying, stdtarget character varying, stdresources character varying, stdappraisalid integer, stdid integer, stdannualplanid integer, stdstatus character varying, stddatestart date, stdddatend date) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.annual_plan(ResultAreas,Target,Resources,AppraisalID,ID,AnnualID,Status,DateStart,DateEnd)
values(stdResultAreas,stdTarget, stdResources,stdAppraisalID,stdID,stdAnnualPlanID,stdStatus,stdDateStart,stdDateEnd);
return 'inserted successfully';
end;
$$;


--
-- Name: appraisal_form(character varying, integer, character varying, integer, date, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.appraisal_form(stddepartment character varying, stdgrade integer, stdposition character varying, stdid integer, stddate date, stdstaffid integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.appraisal_form(Department,Grade,Position,ID,Date,StaffID)
values(stdDepartment,stdGrade,stdPosition,stdID,stdDate,stdStaffId )
;

return 'inserted successfully';
end;
$$;


--
-- Name: competency(character varying, integer, character varying, character varying, integer, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.competency(stdcategory character varying, stdweight integer, stdsub character varying, stdmain character varying, stdid integer, stdappraisalid integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.competency(Category,Weight,Sub,Main,ID,AppraisalID)
values(stdCategory,stdWeight,stdSub,stdMain ,stdID ,stdAppraisalID )

;

return 'inserted successfully';
end;
$$;


--
-- Name: deadline(date, date); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.deadline(stdstart date, stdending date) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.deadline(start_date,ending)
values(stdstart,stdending)
;

return 'inserted successfully';
end;
$$;


--
-- Name: deadline(integer, character varying, date, date); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.deadline(stdid integer, stdtype character varying, stdstart date, stdend date) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.deadline(id,type,Date,start,ending)
values(stdid,stdtype,stdstart,stdend);

return 'inserted successfully';
end;
$$;


--
-- Name: delete_annual_appraisal(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.delete_annual_appraisal(stdid integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
delete from annual_appraisal
where ID=stdid;
return 'Deleted';
	   end;
$$;


--
-- Name: delete_annual_plan(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.delete_annual_plan(stdid integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
delete from annual_plan
where ID=stdid;
return 'Deleted';
	   end;
$$;


--
-- Name: delete_appraisal_form(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.delete_appraisal_form(stdid integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
delete from appraisal_form
where ID=stdid;
return 'Deleted';
	   end;
$$;


--
-- Name: delete_competency(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.delete_competency(stdid integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
delete from competency
where ID=stdid;
return 'Deleted';
	   end;
$$;


--
-- Name: delete_endofyear_review(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.delete_endofyear_review(stdid integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
delete from endofyear_review
where ID=stdid;
return 'Deleted';
	   end;
$$;


--
-- Name: delete_staff(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.delete_staff(stdid integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
delete from staff
where ID=stdid;
return 'Deleted';
	   end;
$$;


--
-- Name: delete_training_recieved(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.delete_training_recieved(stdid integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
delete from training_recieved
where ID=stdid;
return 'Deleted';
	   end;
$$;


--
-- Name: email_insert_trigger_fnc(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.email_insert_trigger_fnc() RETURNS trigger
    LANGUAGE plpgsql
    AS $$

BEGIN
--   NEW.staff."Email" := NEW.hash."email";
INSERT INTO "hash" ( "email")

         VALUES(NEW."Email");
RETURN NEW;

END;

$$;


--
-- Name: endofyear_review(character varying, integer, character varying, integer, integer, character varying, integer, integer, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.endofyear_review(stdassessment character varying, stdscore integer, stdcomment character varying, stdappraisalid integer, stdid integer, stdcompetency character varying, stdannualplanid integer, stdweight integer, stdstatus character varying) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.endofyear_review(Assessment,Score,Comment,AppraisalID,ID,Competency,AnnualPlanID,WeightStatus)
values(stdAssessment,stdScore,stdComment,stdAppraisalID,stdID,stdCompetency,stdAnnualPlanID,stdWeight,stdStatus);
											 
return 'inserted successfully';
end;
$$;


--
-- Name: form(integer, date, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.form(stdappraisalid integer, stddate date, stdstatus character varying) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.Staff(AppraisalID,Date,Status)
values(stdAppraisalID , stdDate,stdStatus);
return 'inserted successfully';
	   end;
$$;


--
-- Name: generate_hash(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.generate_hash() RETURNS text
    LANGUAGE plpgsql
    AS $$
DECLARE
    new_hash text;
    done bool;
BEGIN
    done := false;
    WHILE NOT done LOOP
        new_hash := md5(''||now()::text||random()::text);
        done := NOT exists(SELECT 1 FROM hash WHERE email=new_hash);
    END LOOP;
    RETURN new_hash;
END;
$$;


--
-- Name: get_annual_appraisal(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_annual_appraisal() RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare annual_appraisal_details  jsonb;
begin
select json_agg (annual_appraisal) from annual_appraisal into annual_appraisal_details;
return annual_appraisal_details;
	   end;
$$;


--
-- Name: get_annual_plan(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_annual_plan() RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare annual_plan_details jsonb;
begin
select json_agg (annual_plan) from annual_plan into annual_plan_details ;


return annual_plan_details;
	   end;
$$;


--
-- Name: get_appraisal_form(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_appraisal_form() RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare appraisal_form_details jsonb;
begin
select json_agg (annual_plan) from appraisal_form into appraisal_form_details  ;
return appraisal_form_details;
	   end;
$$;


--
-- Name: get_competency(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_competency() RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare competency_details jsonb;
begin
select json_agg (competency) from competency into competency_details ;

return competency_details ;
	   end;
$$;


--
-- Name: get_deadline(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_deadline() RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare deadline_details  jsonb;
begin
select json_agg (deadline) from deadline into deadline_details ;
return deadline_details;
	   end;
$$;


--
-- Name: get_endofyear_review(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_endofyear_review() RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare endofyear_review_detals jsonb;
begin
select json_agg (endofyear_review) from competency into endofyear_review_detals  ;


return endofyear_review_detals  ;
	   end;
$$;


--
-- Name: get_form(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_form() RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare form_detals jsonb;
begin
select json_agg (form_completion) from form_completion into form_detals ;

return form_detals  ;
	   end;
$$;


--
-- Name: get_hash(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_hash() RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare hash_email jsonb;
begin
select json_agg(quickaccess) from quickaccess into hash_email;
return hash_email;
	   end;
$$;


--
-- Name: get_hash_for_form_details(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_hash_for_form_details() RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare hash_form jsonb;
begin
select json_agg(annual_plan) from annual_plan into hash_form;
return hash_form;
	   end;
$$;


--
-- Name: get_list_of_appraisee(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_list_of_appraisee(user_id integer) RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare list_appraisee jsonb;
declare user_role character varying;
begin
select s.role into user_role from staff s where s.ID=user_id;
if user_role='Admin' then
select json_agg (staff) from staff into list_appraisee;
elsif user_role='Director' then
select json_agg (staff) from staff where supervisor=user_id into list_appraisee;
else 
select '[]'::jsonb into list_appraisee;
end if;
return list_appraisee;
end;
$$;


--
-- Name: get_list_of_completed_form(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_list_of_completed_form() RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare list_completed_form jsonb;
begin
select json_agg ( annual_plan ) from list_completed_form into list_completed_form where status=1;

return  list_completed_form ;
	   end;
$$;


--
-- Name: get_list_of_incomplete_form(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_list_of_incomplete_form() RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare list_incomplete_form jsonb;
begin
select json_agg ( annual_plan ) from list_incomplete_forminto list_completed_form where status=0;

return  list_incomplete_form ;
	   end;
$$;


--
-- Name: get_midyear_review(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_midyear_review() RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare midyear_review_detals jsonb;
begin
select json_agg ( midyear_review) from midyear_review_detals  into midyear_review_detals ;
return midyear_review_detals  ;
	   end;
$$;


--
-- Name: get_staff(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_staff() RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare staff_details jsonb;
begin
select json_agg ( staff) from staff_details into staff_details;
 
return staff_details;
	   end;
$$;


--
-- Name: get_training_recieved(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_training_recieved() RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare training_recieved_details jsonb;
begin
select json_agg (training_recieved) from training_recieved_details into training_recieved_details;

return training_recieved_details   ;
	   end;
$$;


--
-- Name: login(integer, character varying, character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.login(stdstaffid integer, stdusername character varying, stdemail character varying, stdpassword character varying, stdstatus character varying) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.login(StaffID,Username,Email,Password)
values(stdStaffID,stdUsername,stdEmail,stdPassword,stdStatus);

return 'inserted successfully';
end;
$$;


--
-- Name: midyear_review(character varying, character varying, character varying, integer, character varying, integer, integer, date, date); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.midyear_review(stdprogressreview character varying, stdremarks character varying, stdcompetency character varying, stdid integer, stdstatus character varying, stdappraisalid integer, stdannualplanid integer, stddatestart date, stddateend date) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.midyear_review(ProgressReview,Remarks,Competency,ID,Status,AppraisalID,AnnualPlanID,DateStart,DateEnd)
values(stdProgressReview,stdRemarks,stdCompetency,stdID,stdStatus ,stdAppraisalID,stdAnnualPlanID,stdDateStart,stdDateEnd);
return 'inserted successfully';
end;
$$;


--
-- Name: staff(character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.staff(stdid character varying, stdfname character varying, stdsname character varying, stdoname character varying, stdgender character varying, stdsupervisor character varying, stdemail character varying, stdrole character varying) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.Staff(ID,Fname,Sname,Oname,Gender,Supervisor,Email,role)
values(stdID,stdFname,stdSname,stdOname,stdGender,stdSupervisor,stdEmail,stdrole);
return 'inserted successfully';
	   end;
$$;


--
-- Name: training(integer, date, character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.training(stdappraisalid integer, stddate date, stdinstitution character varying, stdprogramme character varying, stdfield character varying) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.Staff(Institution,Programme,Date,Field,AppraisalID)
values(stdAppraisalID ,stdDate,stdInstitution,  stdProgramme ,stdField,stdStatus);
return 'inserted successfully';
	   end;
$$;


--
-- Name: update_annual_appraisal(integer, character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_annual_appraisal(stdgrade integer, stdcomment character varying, stdfield character varying) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin 
update annual_appraisal set Grade=stdgrade,Comment=stdcomment,Field=stdfield
where ID=stdid;
return 'Data Saved';
	   end;
$$;


--
-- Name: update_annual_appraisal_status(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_annual_appraisal_status(stdid integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
update annual_appraisal set Status=1
where ID=stdid;
return 'Status Changed';
	   end;
$$;


--
-- Name: update_annual_plan(integer, character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_annual_plan(stdid integer, stdresultareas character varying, stdtarget character varying, stdresources character varying) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
update annual_plan set ResultAreas=stdresultareas,Target=stdtarget,Resources=stdresources
where ID=stdid;
return 'Data Saved';
	   end;
$$;


--
-- Name: update_annual_plan_status(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_annual_plan_status(stdid integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
update annual_plan set Status=1
where ID=stdid;
return 'Status Changed';
	   end;
$$;


--
-- Name: update_appraisal_form(character varying, integer, integer, date); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_appraisal_form(stddepartment character varying, stdgrade integer, stdid integer, stddate date) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
update appraisal_form set Department=stddepartment,Grade=stdgrade,Date=stddate
where ID=stdid;
return 'Data Saved';
	   end;
$$;


--
-- Name: update_competency(character varying, integer, character varying, character varying, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_competency(stdcategory character varying, stdweight integer, stdsub character varying, stdmain character varying, stdid integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
update competency set Category=stdcategory,Weight=stdweight,Sub=stdsub,Main=stdmain
where ID=stdid;
return 'Data Saved';
	   end;
$$;


--
-- Name: update_deadline(character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_deadline(stdstart character varying, stdend character varying) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin 
update deadline set start=stdstart,ending=stdend
where ID=stdid;
return 'Data Saved';
	   end;
$$;


--
-- Name: update_endofyear_review(character varying, integer, character varying, integer, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_endofyear_review(stdassessment character varying, stdscore integer, stdcomment character varying, stdid integer, stdweight integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
update endofyear_review set Assessment=stdassessment,Score=stdscore,Comment=comment,Weight=stdweight
where ID=stdid;
return 'Data Saved';
	   end;
$$;


--
-- Name: update_endofyyear_review_status(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_endofyyear_review_status(stdid integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
update annual_appraisal set Status=1
where ID=stdid;
return 'Status Changed';
	   end;
$$;


--
-- Name: update_midyear_review(character varying, character varying, character varying, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_midyear_review(stdprogressreview character varying, stdremarks character varying, stdcompetency character varying, stdid integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
update midyear_review set ProgressReview=stdprogressreview,Remarks=stdremarks,Competency=stdcompetency
where ID=stdid;
return 'Data Saved';
	   end;
$$;


--
-- Name: update_midyyear_review_status(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_midyyear_review_status(stdid integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
update annual_appraisal set Status=1
where ID=stdid;
return 'Status Changed';
	   end;
$$;


--
-- Name: update_staff(character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_staff(stdrole character varying) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin 
update staff set role=stdrole
where ID=stdid;
return 'Data Saved';
	   end;
$$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: annual_appraisal; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.annual_appraisal (
    "Grade" integer NOT NULL,
    "Comment" character varying NOT NULL,
    "Field" character varying NOT NULL,
    "AppraisalID" integer NOT NULL,
    "Status" character varying NOT NULL,
    "ID" integer NOT NULL,
    "DateStart" date NOT NULL,
    "DateEnd" date NOT NULL
);


--
-- Name: annual_plan ; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."annual_plan " (
    "ResultAreas" character varying NOT NULL,
    "Target" character varying NOT NULL,
    "Resources" character varying NOT NULL,
    "AppraisalID" integer NOT NULL,
    "ID" integer NOT NULL,
    "AnnualPlanID" integer NOT NULL,
    "Status" character varying NOT NULL,
    "DateStart" date NOT NULL,
    "DateEnd" date NOT NULL
);


--
-- Name: appraisal_form; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.appraisal_form (
    "Department" character varying NOT NULL,
    "Grade" integer NOT NULL,
    "Position" character varying NOT NULL,
    "ID" integer NOT NULL,
    "Date" date NOT NULL,
    "StaffID" integer NOT NULL
);


--
-- Name: competency; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.competency (
    "Category" character varying NOT NULL,
    "Weight" integer NOT NULL,
    "Sub" integer NOT NULL,
    "Main" character varying NOT NULL,
    "ID" integer NOT NULL,
    "AppraisalID" integer NOT NULL
);


--
-- Name: deadline; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.deadline (
    type character varying NOT NULL,
    start_date date NOT NULL,
    ending date NOT NULL,
    id integer NOT NULL
);


--
-- Name: deadline_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.deadline_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: deadline_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.deadline_id_seq OWNED BY public.deadline.id;


--
-- Name: endofyear_review; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.endofyear_review (
    "Assessment" character varying NOT NULL,
    "Score" integer NOT NULL,
    "Comment" character varying NOT NULL,
    "AppraisalID" integer NOT NULL,
    "ID" integer NOT NULL,
    "AnnualPlanID" integer NOT NULL,
    "Weight" integer NOT NULL,
    "Status" character varying NOT NULL
);


--
-- Name: form_completion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.form_completion (
    "ID" integer NOT NULL,
    "Appraisal ID" integer NOT NULL,
    "Date" date NOT NULL,
    "Status" character varying
);


--
-- Name: hash; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hash (
    hash character varying(1000) DEFAULT public.generate_hash() NOT NULL,
    email character varying NOT NULL
);


--
-- Name: logIn; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."logIn" (
    "StaffID" integer NOT NULL,
    "Username" character varying NOT NULL,
    "Email" character varying NOT NULL,
    "Password" character varying NOT NULL
);


--
-- Name: midyear_review; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.midyear_review (
    "ProgressReview" character varying NOT NULL,
    "Remarks" character varying NOT NULL,
    "Competency" character varying NOT NULL,
    "ID" integer NOT NULL,
    "Status" character varying NOT NULL,
    "AppraisalID" integer NOT NULL,
    "AnnualPlanID" integer NOT NULL,
    "DateStart" date NOT NULL,
    "DateEnd" date NOT NULL
);


--
-- Name: quickaccess; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.quickaccess (
    hash character varying NOT NULL,
    email character varying
);


--
-- Name: staff; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.staff (
    id integer NOT NULL,
    "Fname" character varying NOT NULL,
    "Sname" character varying NOT NULL,
    "Oname" character varying NOT NULL,
    "Email" character varying NOT NULL,
    supervisor integer,
    gender public.gender_type,
    role public.role_type
);


--
-- Name: training_recieved; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.training_recieved (
    "ID" integer NOT NULL,
    "Institution" character varying NOT NULL,
    "Programme" character varying NOT NULL,
    "Date" date NOT NULL,
    "Field" character varying NOT NULL,
    "Appraisal ID" integer NOT NULL
);


--
-- Name: deadline id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.deadline ALTER COLUMN id SET DEFAULT nextval('public.deadline_id_seq'::regclass);


--
-- Data for Name: annual_appraisal; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: annual_plan ; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: appraisal_form; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: competency; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: deadline; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: endofyear_review; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: form_completion; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: hash; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.hash (hash, email) VALUES ('84d6d32717678804ec92bc0985041202', 'sjhchasc@gamil.com');
INSERT INTO public.hash (hash, email) VALUES ('5e6fd0286f2d76e93c019655bb44b2ce', 'abshcas@gamail.com');
INSERT INTO public.hash (hash, email) VALUES ('cb44caa45308c8618ca0c72f32134980', 'jgsh@gmail.com');
INSERT INTO public.hash (hash, email) VALUES ('5f221c619d80cc8b2ba3f74f1d774c4d', 'ek@gmail.com');
INSERT INTO public.hash (hash, email) VALUES ('6d172c4e5d851a7c620b12e761f8fe43', 'gshdfhg@yahoo.com
');
INSERT INTO public.hash (hash, email) VALUES ('45c7b06a158ca62707c5d05dad1d6fd9', 'jdshd@gmail.com');
INSERT INTO public.hash (hash, email) VALUES ('3ae8dfacdce9fe071ac45bad18256b6f', 'dhff@gmail.com');


--
-- Data for Name: logIn; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: midyear_review; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: quickaccess; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.quickaccess (hash, email) VALUES ('D09A68B37FB01BA3BDB1F529', NULL);


--
-- Data for Name: staff; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.staff (id, "Fname", "Sname", "Oname", "Email", supervisor, gender, role) VALUES (1, 'prince', 'addo', 'adjei', 'sjhchasc@gamil.com', 3, 'male', 'Director');
INSERT INTO public.staff (id, "Fname", "Sname", "Oname", "Email", supervisor, gender, role) VALUES (2, 'trtry', 'hh', 'llrkr', 'abshcas@gamail.com', 1, 'male', 'Normal');
INSERT INTO public.staff (id, "Fname", "Sname", "Oname", "Email", supervisor, gender, role) VALUES (3, 'lolo
', 'vivi', 'reono', 'jgsh@gmail.com', 3, 'female', 'Admin');
INSERT INTO public.staff (id, "Fname", "Sname", "Oname", "Email", supervisor, gender, role) VALUES (4, 'solo', 'gogo', 'bnbn', 'ek@gmail.com', 1, 'female', 'Normal');
INSERT INTO public.staff (id, "Fname", "Sname", "Oname", "Email", supervisor, gender, role) VALUES (5, 'fofo', 'sasa', 'fefe', 'gshdfhg@yahoo.com
', 3, 'male', 'Director');
INSERT INTO public.staff (id, "Fname", "Sname", "Oname", "Email", supervisor, gender, role) VALUES (6, 'qwq', 'frfr', 'hh', 'jdshd@gmail.com', 5, 'male', 'Normal');
INSERT INTO public.staff (id, "Fname", "Sname", "Oname", "Email", supervisor, gender, role) VALUES (7, 'jdsf', 'kjdks', 'hedf', 'dhff@gmail.com', 5, 'male', 'Normal');


--
-- Data for Name: training_recieved; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Name: deadline_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.deadline_id_seq', 1, false);


--
-- Name: appraisal_form App_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appraisal_form
    ADD CONSTRAINT "App_id" UNIQUE ("ID");


--
-- Name: staff Email; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT "Email" UNIQUE ("Email");


--
-- Name: logIn LogIn_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."logIn"
    ADD CONSTRAINT "LogIn_pkey" PRIMARY KEY ("Username");


--
-- Name: quickaccess QuickAccess_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.quickaccess
    ADD CONSTRAINT "QuickAccess_pkey" PRIMARY KEY (hash);


--
-- Name: staff Staff_id; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT "Staff_id" UNIQUE (id);


--
-- Name: staff Staff_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT "Staff_pkey" PRIMARY KEY (id);


--
-- Name: annual_appraisal annap; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annual_appraisal
    ADD CONSTRAINT annap UNIQUE ("ID");


--
-- Name: annual_plan  annaplan; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."annual_plan "
    ADD CONSTRAINT annaplan UNIQUE ("ID");


--
-- Name: annual_appraisal annual_appraisal_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annual_appraisal
    ADD CONSTRAINT annual_appraisal_pkey PRIMARY KEY ("ID");


--
-- Name: annual_plan  annual_plan _pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."annual_plan "
    ADD CONSTRAINT "annual_plan _pkey" PRIMARY KEY ("ID");


--
-- Name: appraisal_form appraisal_form_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appraisal_form
    ADD CONSTRAINT appraisal_form_pkey PRIMARY KEY ("ID");


--
-- Name: competency competency_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.competency
    ADD CONSTRAINT competency_pkey PRIMARY KEY ("ID");


--
-- Name: deadline deadline_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.deadline
    ADD CONSTRAINT deadline_pkey PRIMARY KEY (id);


--
-- Name: form_completion form_completion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.form_completion
    ADD CONSTRAINT form_completion_pkey PRIMARY KEY ("ID");


--
-- Name: hash hash_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hash
    ADD CONSTRAINT hash_pkey PRIMARY KEY (email);


--
-- Name: endofyear_review midyear_review_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.endofyear_review
    ADD CONSTRAINT midyear_review_pkey PRIMARY KEY ("ID");


--
-- Name: midyear_review midyear_review_pkey1; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.midyear_review
    ADD CONSTRAINT midyear_review_pkey1 PRIMARY KEY ("ID");


--
-- Name: training_recieved training_recieved_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.training_recieved
    ADD CONSTRAINT training_recieved_pkey PRIMARY KEY ("ID");


--
-- Name: staff email_insert_trigger; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER email_insert_trigger AFTER INSERT OR UPDATE ON public.staff FOR EACH ROW EXECUTE FUNCTION public.email_insert_trigger_fnc();


--
-- Name: quickaccess EFK; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.quickaccess
    ADD CONSTRAINT "EFK" FOREIGN KEY (email) REFERENCES public.staff("Email") NOT VALID;


--
-- Name: logIn Staff ID; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."logIn"
    ADD CONSTRAINT "Staff ID" FOREIGN KEY ("StaffID") REFERENCES public.staff(id) NOT VALID;


--
-- Name: training_recieved TAppIdF; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.training_recieved
    ADD CONSTRAINT "TAppIdF" FOREIGN KEY ("Appraisal ID") REFERENCES public.appraisal_form("ID") NOT VALID;


--
-- Name: annual_appraisal anapFK; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annual_appraisal
    ADD CONSTRAINT "anapFK" FOREIGN KEY ("AppraisalID") REFERENCES public.appraisal_form("ID") NOT VALID;


--
-- Name: midyear_review ann; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.midyear_review
    ADD CONSTRAINT ann FOREIGN KEY ("AnnualPlanID") REFERENCES public."annual_plan "("ID") NOT VALID;


--
-- Name: annual_plan  annplnf; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."annual_plan "
    ADD CONSTRAINT annplnf FOREIGN KEY ("AppraisalID") REFERENCES public.appraisal_form("ID") NOT VALID;


--
-- Name: midyear_review apidFK; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.midyear_review
    ADD CONSTRAINT "apidFK" FOREIGN KEY ("AppraisalID") REFERENCES public.appraisal_form("ID") NOT VALID;


--
-- Name: appraisal_form appstaffid; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appraisal_form
    ADD CONSTRAINT appstaffid FOREIGN KEY ("StaffID") REFERENCES public.staff(id) NOT VALID;


--
-- Name: competency comFK; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.competency
    ADD CONSTRAINT "comFK" FOREIGN KEY ("AppraisalID") REFERENCES public.appraisal_form("ID") NOT VALID;


--
-- Name: hash emailfk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hash
    ADD CONSTRAINT emailfk FOREIGN KEY (email) REFERENCES public.staff("Email") NOT VALID;


--
-- Name: endofyear_review eoyFK; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.endofyear_review
    ADD CONSTRAINT "eoyFK" FOREIGN KEY ("AppraisalID") REFERENCES public.appraisal_form("ID") NOT VALID;


--
-- Name: endofyear_review eoyapFK; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.endofyear_review
    ADD CONSTRAINT "eoyapFK" FOREIGN KEY ("AnnualPlanID") REFERENCES public."annual_plan "("ID") NOT VALID;


--
-- Name: form_completion fcomFK; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.form_completion
    ADD CONSTRAINT "fcomFK" FOREIGN KEY ("Appraisal ID") REFERENCES public.appraisal_form("ID");


--
-- PostgreSQL database dump complete
--

