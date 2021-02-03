--
-- PostgreSQL database dump
--

-- Dumped from database version 12.5 (Ubuntu 12.5-0ubuntu0.20.10.1)
-- Dumped by pg_dump version 12.5 (Ubuntu 12.5-0ubuntu0.20.10.1)

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
-- Name: add_staff(character varying, character varying, character varying, character varying, integer, character varying, character varying, character varying, character varying, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.add_staff(stdfname character varying, stdsname character varying, stdoname character varying, stdgender character varying, stdsupervisor integer, stdemail character varying, stdrole character varying, stddepartment character varying, stdposition character varying, stdgrade integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.staff(fname,sname,oname,gender,supervisor,email,role,department,position,grade)
values(stdfname,stdsname,stdoname,stdgender,stdsupervisor,stdemail,stdrole,stddepartment,stdposition,stdgrade);
return 'inserted successfully';
	   end;
$$;


--
-- Name: annual_appraisal(integer, character varying, character varying, integer, character varying, bigint); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.annual_appraisal(stdgrade integer, stdcomment character varying, stdfield character varying, stdappraisalid integer, stdstatus character varying, stdannual_appraisal_id bigint) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.annual_appraisal(grade,comment,field,appraisal_id,status,annual_appraisal_id)
values(stdGrade ,stdComment ,stdField,stdAppraisalID,stdStatus,stdID,stdDateStart,stdDateEnd);
return 'inserted successfully';
	   end;
$$;


--
-- Name: annual_plan(character varying, character varying, character varying, integer, bigint, integer, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.annual_plan(stdresultareas character varying, stdtarget character varying, stdresources character varying, stdappraisalid integer, stdannualplanid bigint, stdstatus integer, stdform_hash character varying) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.annual_plan(result_areas,target,resources,appraisal_id,annual_paln_id,status,form_hash)
values(stdresult_areas,stdtarget, stdresources,stdappraisal_id,stdannual_plan_id,stdstatus);
return 'inserted successfully';
end;
$$;


--
-- Name: appraisal_form(character varying, integer, character varying, bigint, date, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.appraisal_form(stddepartment character varying, stdgrade integer, stdposition character varying, stdappraisal_form_id bigint, stddate date, stdstaffid integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.appraisal_form(department,grade,position,appraisal_form_id,date,staff_id)
values(stddepartment,stdgrade,stdposition,stdappraisal_form_id,stddate,stdstaff_Id)
;

return 'inserted successfully';
end;
$$;


--
-- Name: appraisalformid_insert_trigger_fnc(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.appraisalformid_insert_trigger_fnc() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN

INSERT INTO "annual_plan"("appraisal_form_id")

         VALUES(NEW."appraisal_form_id");
RETURN NEW;

END;
$$;


--
-- Name: competency(character varying, integer, character varying, character varying, bigint, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.competency(stdcategory character varying, stdweight integer, stdsub character varying, stdmain character varying, stdcompetency_id bigint, stdappraisal_id integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.competency(category,weight,sub,main,competency_id,appraisal_id)
values(stdcategory,stdweight,stdsub,stdmain ,stdcompetency_id ,stdappraisal_id )

;

return 'inserted successfully';
end;
$$;


--
-- Name: deadline(character varying, date, date, bigint); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.deadline(stddeadline_type character varying, stdstart date, stdending date, stddeadline_id bigint) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.deadline(deadline_type,start_date,ending,deadline_id)
values(stddeadline_type,stdstart,stdending)
;

return 'inserted successfully';
end;
$$;


--
-- Name: delete_annual_appraisal(bigint); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.delete_annual_appraisal(stdannual_appraisal_id bigint) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
delete from annual_appraisal
where staff_id=stdannual_appraisal_id;
return 'Deleted';
	   end;
$$;


--
-- Name: delete_annual_plan(bigint); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.delete_annual_plan(stdannual_plan_id bigint) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
delete from annual_plan
where staff_id=stdannual_plan_id;
return 'Deleted';
	   end;
$$;


--
-- Name: delete_appraisal_form(bigint); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.delete_appraisal_form(stdappraisal_form_id bigint) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
delete from appraisal_form
where staff_id=stdappraisal_form_id;
return 'Deleted';
	   end;
$$;


--
-- Name: delete_competency(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.delete_competency(stdcompetency_id integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
delete from competency
where staff_id=stdcompetency_id;
return 'Deleted';
	   end;
$$;


--
-- Name: delete_endofyear_review(bigint); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.delete_endofyear_review(stdendofyear_review_id bigint) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
delete from endofyear_review
where staff_id=stdendofyear_review_id;
return 'Deleted';
	   end;
$$;


--
-- Name: delete_staff(bigint); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.delete_staff(stdstaff_id bigint) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
delete from staff
where staff_id=stdstaff_id;
return 'Deleted';
	   end;
$$;


--
-- Name: delete_training_recieved(bigint); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.delete_training_recieved(stdtraining_recieved_id bigint) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
delete from training_recieved
where ID=stdtraining_recieved_id;
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
INSERT INTO "hash_table" ( "email")

         VALUES(NEW."email");
RETURN NEW;

END;
$$;


--
-- Name: endofyear_review(character varying, integer, character varying, integer, bigint, integer, integer, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.endofyear_review(stdassessment character varying, stdscore integer, stdcomment character varying, stdappraisal_id integer, stdendofyear_reviewid bigint, stdannual_plan_id integer, stdweight integer, stdstatus integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.endofyear_review(assessment,score,comment,appraisal_id,endofyear_review_id,annual_plan_id,weight,status)
values(stdassessment,stdscore,stdcomment,stdappraisal_id,stdendofyear_review_id,stdannual_plan_id,stdweight,stdstatus);
											 
return 'inserted successfully';
end;
$$;


--
-- Name: generate_appraisal_form_id(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.generate_appraisal_form_id() RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare 
type_date date;
generate integer;
begin
select start_date from deadline into type_date;
if type_date=now() then select appraisal_form_id from appraisal_form into generate;
else  return 'The film could not be found'; 
return generate;
end if;
end;
$$;


--
-- Name: generate_hash(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.generate_hash() RETURNS text
    LANGUAGE plpgsql
    AS $$
DECLARE
   ddate date;
  hash character varying;
BEGIN
    select start_date from deadline into ddate where start_date=start_date;
  if not found then
  raise notice'date mismatch';	  		
else  select md5(''||now()::text||random()::text) into hash;
  end if;
    RETURN hash;
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
select json_agg (appraisal_form) from appraisal_form into appraisal_form_details  ;
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
declare endofyear_review_details jsonb;
begin
select json_agg (endofyear_review) from endofyear_review into endofyear_review_details  ;

return endofyear_review_details  ;
	   end;
$$;


--
-- Name: get_entire_hash_table(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_entire_hash_table() RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare hash_email jsonb;
begin
select json_agg(hash_table) from hash_table into hash_email;
return hash_email;
	   end;
$$;


--
-- Name: get_form_details_yearly(integer, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_form_details_yearly(vstaff_id integer, vform_year integer) RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare results jsonb; 
begin
SELECT json_agg (form_details) FROM (
	SELECT
	appraisal_form.appraisal_form_id,
	extract(year from appraisal_form.date) as appraisal_year,
	staff.fname as firstname,
	staff.sname as lastname,
	staff.oname as middlename,
	staff.email,
	staff.gender,
	yearly_details.department,
	yearly_details.position,
	yearly_details.grade,	
	annual_plan.result_areas,
	annual_plan.target,
	annual_plan.resources,
	midyear_review.progress_review,
	midyear_review.remarks,
	endofyear_review.assessment,
	endofyear_review.score,
	endofyear_review.comment,
	endofyear_review.weight
		
FROM
	staff 
INNER JOIN appraisal_form  
    ON staff.staff_id=appraisal_form.staff_id
INNER JOIN yearly_details  
    ON staff.staff_id=yearly_details.staff_id	
	RIGHT JOIN annual_plan  
    ON appraisal_form.appraisal_form_id=annual_plan.appraisal_form_id
	RIGHT JOIN midyear_review  
    ON appraisal_form.appraisal_form_id = midyear_review.appraisal_form_id
	RIGHT JOIN endofyear_review  
    ON appraisal_form.appraisal_form_id  =endofyear_review  .appraisal_form_id
	WHERE staff.staff_id = vstaff_id 
	AND appraisal_form.date is null OR extract(year from appraisal_form.date) = vform_year
	AND extract(year from yearly_details.year) = vform_year) form_details into results; 
RETURN results;	
	   end;
$$;


--
-- Name: get_hash_verification(character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.get_hash_verification(stdhash character varying) RETURNS jsonb
    LANGUAGE plpgsql
    AS $$
declare
verified bool;
user_email character varying;
user_details jsonb;
begin
select exists(select email from hash_table where hash=stdhash) into verified;
if verified='true' then
select email from hash_table where hash=stdhash into user_email;
select json_agg(json_build_object('fname',staff.fname,'sname',staff.staff_id,'department',appraisal_form.department,'grade',appraisal_form.grade,'position',appraisal_form.position))
from staff inner join appraisal_form on appraisal_form.staff_id=staff.staff_id where staff.email=user_email
into user_details;
else
select '[]'::jsonb into user_details;
end if;

return user_details;
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
select s.role into user_role from staff s where s.staff_id=user_id;
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
declare midyear_review_details jsonb;
begin
select json_agg ( midyear_review) from midyear_review_details  into midyear_review_details ;
return midyear_review_details  ;
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
select json_agg ( staff) from staff into staff_details;
 
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
-- Name: hash_insert_trigger_fnc(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.hash_insert_trigger_fnc() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN

INSERT INTO public.annual_plan("form_hash")

         VALUES(NEW."hash");
RETURN NEW;

END;
$$;


--
-- Name: login(integer, character varying, character varying, character varying, bigint); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.login(stdstaff_id integer, stdusername character varying, stdemail character varying, stdpassword character varying, stdlogin_id bigint) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.login(staff_id,username,email,password,login_id)
values(stdstaff_id,stdusername,stdemail,stdpassword,stdlogin_id);

return 'inserted successfully';
end;
$$;


--
-- Name: midyear_review(bigint, character varying, character varying, integer, integer, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.midyear_review(stdmidyear_review_id bigint, stdprogress_review character varying, stdremarks character varying, stdstatus integer, stdappraisal_id integer, stdannual_plan_id integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.midyear_review(midyear_review_id,progress_review_id,remarks,status,appraisal_id,annual_plan_id)
values(stdmidyear_review_id,stdprogress_review,stdremarks,stdstatus ,stdappraisal_id,stdannual_plan_id);
return 'inserted successfully';
end;
$$;


--
-- Name: training_recieved(bigint, character varying, character varying, date, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.training_recieved(stdtraining_recieved_id bigint, stdinstitution character varying, stdprogramme character varying, stddate date, stdappraisal_id integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.Staff(training_recieved_id,institution,programme,date,appraisal_id)
values(stdtarining_recieved_id,stdinstitution,stdProgramme,date ,stdappraisal_id);
return 'inserted successfully';
	   end;
$$;


--
-- Name: update_annual_appraisal_status(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_annual_appraisal_status(stdannual_appraisal_id integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
update annual_appraisal set Status=1
where annual_appraisal=stdannual_appraisal_id;
return 'Status Changed';
	   end;
$$;


--
-- Name: update_annual_plan_status(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_annual_plan_status(stdannual_plan_id integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
update annual_plan set Status=1
where annual_plan_id=stdannual_plan_id;
return 'Status Changed';
	   end;
$$;


--
-- Name: update_endofyyear_review_status(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_endofyyear_review_status(stdendofyear_review_id integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
update annual_appraisal set Status=1
where annual_appraisal=stdendofyear_review_id;
return 'Status Changed';
	   end;
$$;


--
-- Name: update_midyyear_review_status(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_midyyear_review_status(stdmidyyear_review_id integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
update annual_appraisal set Status=1
where annual_appraisal=stdmidyyear_review_id;
return 'Status Changed';
	   end;
$$;


--
-- Name: yearly_details(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.yearly_details() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	
		 INSERT INTO "yearly_details"("department","grade","position","staff_id")
		 VALUES(new."department",new."grade",new."position",new."staff_id");

	RETURN NEW;
END;
$$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: annual_appraisal; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.annual_appraisal (
    grade integer NOT NULL,
    comment character varying NOT NULL,
    field character varying NOT NULL,
    appraisal_form_id bigint NOT NULL,
    status character varying NOT NULL,
    annual_appraisal_id integer NOT NULL
);


--
-- Name: annual_appraisal_appraisal_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.annual_appraisal_appraisal_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: annual_appraisal_appraisal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.annual_appraisal_appraisal_id_seq OWNED BY public.annual_appraisal.appraisal_form_id;


--
-- Name: annual_plan; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.annual_plan (
    result_areas character varying,
    target character varying,
    resources character varying,
    appraisal_form_id integer,
    annual_plan_id bigint NOT NULL,
    status integer DEFAULT 0,
    form_hash character varying
);


--
-- Name: annual_plan _annual_plan_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."annual_plan _annual_plan_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: annual_plan _annual_plan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."annual_plan _annual_plan_id_seq" OWNED BY public.annual_plan.annual_plan_id;


--
-- Name: appraisal_form; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.appraisal_form (
    department character varying NOT NULL,
    grade integer NOT NULL,
    "position" character varying NOT NULL,
    appraisal_form_id bigint NOT NULL,
    date date NOT NULL,
    staff_id integer NOT NULL
);


--
-- Name: appraisal_form_appraisal_form_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.appraisal_form_appraisal_form_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: appraisal_form_appraisal_form_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.appraisal_form_appraisal_form_id_seq OWNED BY public.appraisal_form.appraisal_form_id;


--
-- Name: competency; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.competency (
    category character varying NOT NULL,
    weight integer NOT NULL,
    sub integer NOT NULL,
    main character varying NOT NULL,
    competency_id bigint NOT NULL,
    appraisal_form_id integer NOT NULL
);


--
-- Name: competency_competency_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.competency_competency_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: competency_competency_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.competency_competency_id_seq OWNED BY public.competency.competency_id;


--
-- Name: deadline; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.deadline (
    deadline_type character varying NOT NULL,
    start_date date,
    ending date NOT NULL,
    deadline_id bigint NOT NULL
);


--
-- Name: deadline_deadline_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.deadline_deadline_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: deadline_deadline_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.deadline_deadline_id_seq OWNED BY public.deadline.deadline_id;


--
-- Name: endofyear_review; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.endofyear_review (
    assessment character varying,
    score integer,
    comment character varying,
    appraisal_form_id integer,
    endofyear_review_id bigint NOT NULL,
    annual_plan_id integer,
    weight integer,
    status integer DEFAULT 0
);


--
-- Name: endofyear_review_endofyear_review_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.endofyear_review_endofyear_review_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: endofyear_review_endofyear_review_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.endofyear_review_endofyear_review_id_seq OWNED BY public.endofyear_review.endofyear_review_id;


--
-- Name: form_completion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.form_completion (
    form_completion_id bigint NOT NULL,
    appraisal_id integer,
    date date,
    status integer
);


--
-- Name: form_completion_form_completion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.form_completion_form_completion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: form_completion_form_completion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.form_completion_form_completion_id_seq OWNED BY public.form_completion.form_completion_id;


--
-- Name: hash_table; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hash_table (
    hash character varying(1000) DEFAULT public.generate_hash() NOT NULL,
    email character varying,
    hash_table_id bigint NOT NULL
);


--
-- Name: hash_table_hash_table_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.hash_table_hash_table_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: hash_table_hash_table_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.hash_table_hash_table_id_seq OWNED BY public.hash_table.hash_table_id;


--
-- Name: logIn; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."logIn" (
    staff_id integer NOT NULL,
    username character varying NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL,
    login_id bigint NOT NULL
);


--
-- Name: logIn_login_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."logIn_login_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: logIn_login_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."logIn_login_id_seq" OWNED BY public."logIn".login_id;


--
-- Name: midyear_review; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.midyear_review (
    midyear_review_id bigint NOT NULL,
    progress_review character varying,
    remarks character varying,
    status integer DEFAULT 0,
    appraisal_form_id integer,
    annual_plan_id integer
);


--
-- Name: midyear_review_midyear_review_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.midyear_review_midyear_review_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: midyear_review_midyear_review_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.midyear_review_midyear_review_id_seq OWNED BY public.midyear_review.midyear_review_id;


--
-- Name: staff; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.staff (
    staff_id bigint NOT NULL,
    fname character varying NOT NULL,
    sname character varying NOT NULL,
    oname character varying NOT NULL,
    email character varying NOT NULL,
    supervisor integer NOT NULL,
    gender character varying NOT NULL,
    role character varying NOT NULL,
    department character varying NOT NULL,
    "position" character varying NOT NULL,
    grade integer NOT NULL
);


--
-- Name: staff_staff_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.staff_staff_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: staff_staff_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.staff_staff_id_seq OWNED BY public.staff.staff_id;


--
-- Name: training_recieved; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.training_recieved (
    training_recieved_id bigint NOT NULL,
    institution character varying NOT NULL,
    programme character varying NOT NULL,
    date date NOT NULL,
    appraisal_id integer NOT NULL
);


--
-- Name: training_recieved_training_recieved_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.training_recieved_training_recieved_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: training_recieved_training_recieved_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.training_recieved_training_recieved_id_seq OWNED BY public.training_recieved.training_recieved_id;


--
-- Name: yearly_details; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.yearly_details (
    department character varying NOT NULL,
    grade integer NOT NULL,
    "position" character varying NOT NULL,
    year date DEFAULT now() NOT NULL,
    staff_id integer NOT NULL,
    yearly_details_id bigint NOT NULL
);


--
-- Name: yearly_details_yearly_details_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.yearly_details_yearly_details_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: yearly_details_yearly_details_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.yearly_details_yearly_details_id_seq OWNED BY public.yearly_details.yearly_details_id;


--
-- Name: annual_appraisal appraisal_form_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annual_appraisal ALTER COLUMN appraisal_form_id SET DEFAULT nextval('public.annual_appraisal_appraisal_id_seq'::regclass);


--
-- Name: annual_plan annual_plan_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annual_plan ALTER COLUMN annual_plan_id SET DEFAULT nextval('public."annual_plan _annual_plan_id_seq"'::regclass);


--
-- Name: appraisal_form appraisal_form_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appraisal_form ALTER COLUMN appraisal_form_id SET DEFAULT nextval('public.appraisal_form_appraisal_form_id_seq'::regclass);


--
-- Name: competency competency_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.competency ALTER COLUMN competency_id SET DEFAULT nextval('public.competency_competency_id_seq'::regclass);


--
-- Name: deadline deadline_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.deadline ALTER COLUMN deadline_id SET DEFAULT nextval('public.deadline_deadline_id_seq'::regclass);


--
-- Name: endofyear_review endofyear_review_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.endofyear_review ALTER COLUMN endofyear_review_id SET DEFAULT nextval('public.endofyear_review_endofyear_review_id_seq'::regclass);


--
-- Name: form_completion form_completion_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.form_completion ALTER COLUMN form_completion_id SET DEFAULT nextval('public.form_completion_form_completion_id_seq'::regclass);


--
-- Name: hash_table hash_table_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hash_table ALTER COLUMN hash_table_id SET DEFAULT nextval('public.hash_table_hash_table_id_seq'::regclass);


--
-- Name: logIn login_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."logIn" ALTER COLUMN login_id SET DEFAULT nextval('public."logIn_login_id_seq"'::regclass);


--
-- Name: midyear_review midyear_review_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.midyear_review ALTER COLUMN midyear_review_id SET DEFAULT nextval('public.midyear_review_midyear_review_id_seq'::regclass);


--
-- Name: staff staff_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.staff ALTER COLUMN staff_id SET DEFAULT nextval('public.staff_staff_id_seq'::regclass);


--
-- Name: training_recieved training_recieved_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.training_recieved ALTER COLUMN training_recieved_id SET DEFAULT nextval('public.training_recieved_training_recieved_id_seq'::regclass);


--
-- Name: yearly_details yearly_details_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yearly_details ALTER COLUMN yearly_details_id SET DEFAULT nextval('public.yearly_details_yearly_details_id_seq'::regclass);


--
-- Data for Name: annual_appraisal; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: annual_plan; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.annual_plan (result_areas, target, resources, appraisal_form_id, annual_plan_id, status, form_hash) VALUES ('Everything', 'Execute', 'Good', 16, 32, 1, '96ba5594d7d04f71150a81c417f53a34');
INSERT INTO public.annual_plan (result_areas, target, resources, appraisal_form_id, annual_plan_id, status, form_hash) VALUES (NULL, NULL, NULL, NULL, 34, 1, '60e8beba18e9a8550e725038b584df17');
INSERT INTO public.annual_plan (result_areas, target, resources, appraisal_form_id, annual_plan_id, status, form_hash) VALUES (NULL, NULL, NULL, NULL, 33, 1, '777179eebfcc3fee3648cbfc6fb3ea86');


--
-- Data for Name: appraisal_form; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.appraisal_form (department, grade, "position", appraisal_form_id, date, staff_id) VALUES ('Research', 100, 'Developer', 16, '2021-02-20', 1);


--
-- Data for Name: competency; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.competency (category, weight, sub, main, competency_id, appraisal_form_id) VALUES ('Body', 10, 12, 'Coder', 1, 16);


--
-- Data for Name: deadline; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.deadline (deadline_type, start_date, ending, deadline_id) VALUES ('Start', '2021-02-20', '2021-03-30', 1);
INSERT INTO public.deadline (deadline_type, start_date, ending, deadline_id) VALUES ('Mid', '2021-03-30', '2020-08-08', 2);
INSERT INTO public.deadline (deadline_type, start_date, ending, deadline_id) VALUES ('End', '2021-04-02', '2021-08-21', 3);


--
-- Data for Name: endofyear_review; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.endofyear_review (assessment, score, comment, appraisal_form_id, endofyear_review_id, annual_plan_id, weight, status) VALUES ('Well Done', 100, 'improve', 16, 1, 32, 200, 1);


--
-- Data for Name: form_completion; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: hash_table; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.hash_table (hash, email, hash_table_id) VALUES ('96ba5594d7d04f71150a81c417f53a34', 'paddo144@gmail.com', 39);
INSERT INTO public.hash_table (hash, email, hash_table_id) VALUES ('777179eebfcc3fee3648cbfc6fb3ea86', 'great@gamil.com', 40);


--
-- Data for Name: logIn; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public."logIn" (staff_id, username, email, password, login_id) VALUES (1, 'iwan', 'paddo144@gmail.com', 'asdd', 1);
INSERT INTO public."logIn" (staff_id, username, email, password, login_id) VALUES (23, 'sammy', 'sammy@gmail.com', 'dcd', 5);


--
-- Data for Name: midyear_review; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: staff; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.staff (staff_id, fname, sname, oname, email, supervisor, gender, role, department, "position", grade) VALUES (1, 'PRINCE', 'ADDO', 'ADEJI', 'paddo144@gmail.com', 1, 'male', 'Admin', 'Research', 'Manager', 100);
INSERT INTO public.staff (staff_id, fname, sname, oname, email, supervisor, gender, role, department, "position", grade) VALUES (23, 'SAMMY', 'AKI', 'PAWPAW', 'great@gamil.com', 2, 'male', 'Director', 'Consultancy', 'Developer', 90);


--
-- Data for Name: training_recieved; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: yearly_details; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.yearly_details (department, grade, "position", year, staff_id, yearly_details_id) VALUES ('Research', 100, 'Manager', '2021-01-29', 1, 22);
INSERT INTO public.yearly_details (department, grade, "position", year, staff_id, yearly_details_id) VALUES ('Consultancy', 90, 'Developer', '2021-01-29', 23, 23);


--
-- Name: annual_appraisal_appraisal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.annual_appraisal_appraisal_id_seq', 1, false);


--
-- Name: annual_plan _annual_plan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."annual_plan _annual_plan_id_seq"', 34, true);


--
-- Name: appraisal_form_appraisal_form_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.appraisal_form_appraisal_form_id_seq', 16, true);


--
-- Name: competency_competency_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.competency_competency_id_seq', 1, false);


--
-- Name: deadline_deadline_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.deadline_deadline_id_seq', 4, true);


--
-- Name: endofyear_review_endofyear_review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.endofyear_review_endofyear_review_id_seq', 1, false);


--
-- Name: form_completion_form_completion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.form_completion_form_completion_id_seq', 1, false);


--
-- Name: hash_table_hash_table_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.hash_table_hash_table_id_seq', 41, true);


--
-- Name: logIn_login_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."logIn_login_id_seq"', 5, true);


--
-- Name: midyear_review_midyear_review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.midyear_review_midyear_review_id_seq', 1, false);


--
-- Name: staff_staff_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.staff_staff_id_seq', 23, true);


--
-- Name: training_recieved_training_recieved_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.training_recieved_training_recieved_id_seq', 1, false);


--
-- Name: yearly_details_yearly_details_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.yearly_details_yearly_details_id_seq', 23, true);


--
-- Name: annual_plan ann_plan_uq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annual_plan
    ADD CONSTRAINT ann_plan_uq UNIQUE (annual_plan_id);


--
-- Name: annual_appraisal ann_uq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annual_appraisal
    ADD CONSTRAINT ann_uq UNIQUE (annual_appraisal_id);


--
-- Name: annual_appraisal annual_appraisal_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annual_appraisal
    ADD CONSTRAINT annual_appraisal_pkey PRIMARY KEY (annual_appraisal_id);


--
-- Name: annual_plan annual_plan _pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annual_plan
    ADD CONSTRAINT "annual_plan _pkey" PRIMARY KEY (annual_plan_id);


--
-- Name: appraisal_form app_uq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appraisal_form
    ADD CONSTRAINT app_uq UNIQUE (appraisal_form_id);


--
-- Name: appraisal_form appraisal_form_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appraisal_form
    ADD CONSTRAINT appraisal_form_pkey PRIMARY KEY (appraisal_form_id);


--
-- Name: competency competency_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.competency
    ADD CONSTRAINT competency_pkey PRIMARY KEY (competency_id);


--
-- Name: deadline deadline_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.deadline
    ADD CONSTRAINT deadline_pkey PRIMARY KEY (deadline_id);


--
-- Name: staff email_uq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT email_uq UNIQUE (email);


--
-- Name: endofyear_review endofyear_review_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.endofyear_review
    ADD CONSTRAINT endofyear_review_pkey PRIMARY KEY (endofyear_review_id);


--
-- Name: form_completion form_completion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.form_completion
    ADD CONSTRAINT form_completion_pkey PRIMARY KEY (form_completion_id);


--
-- Name: hash_table hash_table_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hash_table
    ADD CONSTRAINT hash_table_pkey PRIMARY KEY (hash_table_id);


--
-- Name: logIn logIn_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."logIn"
    ADD CONSTRAINT "logIn_pkey" PRIMARY KEY (login_id);


--
-- Name: midyear_review midyear_review_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.midyear_review
    ADD CONSTRAINT midyear_review_pkey PRIMARY KEY (midyear_review_id);


--
-- Name: staff staff_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT staff_pkey PRIMARY KEY (staff_id);


--
-- Name: staff staff_uq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT staff_uq UNIQUE (staff_id);


--
-- Name: training_recieved training_recieved_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.training_recieved
    ADD CONSTRAINT training_recieved_pkey PRIMARY KEY (training_recieved_id);


--
-- Name: yearly_details yearly_details_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yearly_details
    ADD CONSTRAINT yearly_details_pkey PRIMARY KEY (yearly_details_id);


--
-- Name: appraisal_form appraisalformid_insert_trigger; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER appraisalformid_insert_trigger AFTER INSERT ON public.appraisal_form FOR EACH ROW EXECUTE FUNCTION public.appraisalformid_insert_trigger_fnc();


--
-- Name: staff email_insert_trigger; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER email_insert_trigger AFTER INSERT OR UPDATE ON public.staff FOR EACH ROW EXECUTE FUNCTION public.email_insert_trigger_fnc();


--
-- Name: hash_table hash_insert_trigger; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER hash_insert_trigger AFTER INSERT ON public.hash_table FOR EACH ROW EXECUTE FUNCTION public.hash_insert_trigger_fnc();


--
-- Name: staff yearly_details; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER yearly_details AFTER INSERT ON public.staff FOR EACH ROW EXECUTE FUNCTION public.yearly_details();


--
-- Name: annual_appraisal ann_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annual_appraisal
    ADD CONSTRAINT ann_fk FOREIGN KEY (appraisal_form_id) REFERENCES public.appraisal_form(appraisal_form_id) NOT VALID;


--
-- Name: annual_plan ann_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annual_plan
    ADD CONSTRAINT ann_fk FOREIGN KEY (appraisal_form_id) REFERENCES public.appraisal_form(appraisal_form_id) NOT VALID;


--
-- Name: appraisal_form app_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appraisal_form
    ADD CONSTRAINT app_fk FOREIGN KEY (staff_id) REFERENCES public.staff(staff_id) NOT VALID;


--
-- Name: endofyear_review end_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.endofyear_review
    ADD CONSTRAINT end_fk FOREIGN KEY (appraisal_form_id) REFERENCES public.appraisal_form(appraisal_form_id) NOT VALID;


--
-- Name: endofyear_review end_fk_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.endofyear_review
    ADD CONSTRAINT end_fk_2 FOREIGN KEY (annual_plan_id) REFERENCES public.annual_plan(annual_plan_id) NOT VALID;


--
-- Name: form_completion form_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.form_completion
    ADD CONSTRAINT form_fk FOREIGN KEY (appraisal_id) REFERENCES public.appraisal_form(appraisal_form_id) NOT VALID;


--
-- Name: hash_table hash_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hash_table
    ADD CONSTRAINT hash_fk FOREIGN KEY (email) REFERENCES public.staff(email) NOT VALID;


--
-- Name: logIn login_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."logIn"
    ADD CONSTRAINT login_fk FOREIGN KEY (staff_id) REFERENCES public.staff(staff_id) NOT VALID;


--
-- Name: midyear_review mid2_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.midyear_review
    ADD CONSTRAINT mid2_fk FOREIGN KEY (appraisal_form_id) REFERENCES public.appraisal_form(appraisal_form_id) NOT VALID;


--
-- Name: midyear_review mid_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.midyear_review
    ADD CONSTRAINT mid_fk FOREIGN KEY (annual_plan_id) REFERENCES public.annual_plan(annual_plan_id) NOT VALID;


--
-- Name: training_recieved train_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.training_recieved
    ADD CONSTRAINT train_fk FOREIGN KEY (appraisal_id) REFERENCES public.appraisal_form(appraisal_form_id) NOT VALID;


--
-- Name: yearly_details year_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.yearly_details
    ADD CONSTRAINT year_fk FOREIGN KEY (staff_id) REFERENCES public.staff(staff_id) NOT VALID;


--
-- PostgreSQL database dump complete
--

