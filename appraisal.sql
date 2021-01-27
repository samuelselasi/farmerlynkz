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
-- Name: annual_appraisal(integer, character varying, character varying, integer, character varying, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.annual_appraisal(stdgrade integer, stdcomment character varying, stdfield character varying, stdappraisalid integer, stdstatus character varying, stdannual_appraisal_id integer) RETURNS character varying
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
-- Name: annual_plan(character varying, character varying, character varying, integer, integer, integer, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.annual_plan(stdresultareas character varying, stdtarget character varying, stdresources character varying, stdappraisalid integer, stdannualplanid integer, stdstatus integer, stdform_hash character varying) RETURNS character varying
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
-- Name: appraisal_form(character varying, integer, character varying, integer, date, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.appraisal_form(stddepartment character varying, stdgrade integer, stdposition character varying, stdappraisal_form_id integer, stddate date, stdstaffid integer) RETURNS character varying
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
-- Name: competency(character varying, integer, character varying, character varying, integer, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.competency(stdcategory character varying, stdweight integer, stdsub character varying, stdmain character varying, stdcompetency_id integer, stdappraisal_id integer) RETURNS character varying
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
-- Name: deadline(character varying, date, date, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.deadline(stdtype character varying, stdstart date, stdending date, stddeadline_id integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.deadline(type,start_date,ending,deadline_id)
values(stdstart,stdending)
;

return 'inserted successfully';
end;
$$;


--
-- Name: delete_annual_appraisal(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.delete_annual_appraisal(stdannual_appraisal_id integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
delete from annual_appraisal
where ID=stdannual_appraisal_id;
return 'Deleted';
	   end;
$$;


--
-- Name: delete_annual_plan(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.delete_annual_plan(stdannual_plan_id integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
delete from annual_plan
where ID=stdannual_plan_id;
return 'Deleted';
	   end;
$$;


--
-- Name: delete_appraisal_form(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.delete_appraisal_form(stdappraisal_form_id integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
delete from appraisal_form
where ID=stdappraisal_form_id;
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
where ID=stdcompetency_id;
return 'Deleted';
	   end;
$$;


--
-- Name: delete_endofyear_review(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.delete_endofyear_review(stdendofyear_review_id integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
delete from endofyear_review
where ID=stdendofyear_review_id;
return 'Deleted';
	   end;
$$;


--
-- Name: delete_staff(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.delete_staff(stdstaff_id integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
delete from staff
where ID=stdstaff_id;
return 'Deleted';
	   end;
$$;


--
-- Name: delete_training_recieved(integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.delete_training_recieved(stdtraining_recieved_id integer) RETURNS character varying
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
-- Name: endofyear_review(character varying, integer, character varying, integer, integer, integer, integer, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.endofyear_review(stdassessment character varying, stdscore integer, stdcomment character varying, stdappraisal_id integer, stdendofyear_reviewid integer, stdannual_plan_id integer, stdweight integer, stdstatus integer) RETURNS character varying
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
select json_agg(hash_table) from hash_table into hash_email;
return hash_email;
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
select exists(select email from hash where hash=stdhash) into verified;
if verified='true' then
select email from hash where hash=stdhash into user_email;
select json_agg(json_build_object('fname',staff.faname,'sname',staff.sname,'oname',staff.oname,'department',appraisal_form.department, appraisal_form.position))
from staff inner join appraisal_form on appraisal_form.staff_id=staff.id where staff.email=user_email
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
-- Name: hash_insert_trigger_fnc(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.hash_insert_trigger_fnc() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN

INSERT INTO public."annual_plan"("form_hash")

         VALUES(NEW."hash");
RETURN NEW;

END;
$$;


--
-- Name: login(integer, character varying, character varying, character varying, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.login(stdstaff_id integer, stdusername character varying, stdemail character varying, stdpassword character varying, stdlogin_id integer) RETURNS character varying
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
-- Name: midyear_review(integer, character varying, character varying, integer, integer, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.midyear_review(stdmidyear_review_id integer, stdprogress_review character varying, stdremarks character varying, stdstatus integer, stdappraisal_id integer, stdannual_plan_id integer) RETURNS character varying
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
-- Name: staff(character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, character varying, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.staff(stdstaff_id character varying, stdfname character varying, stdsname character varying, stdoname character varying, stdgender character varying, stdsupervisor character varying, stdemail character varying, stdrole character varying, stddepartment character varying, stdposition character varying, stdgrade integer) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.Staff(staff_id,fname,sname,oname,gender,supervisor,email,role,department,position,grade)
values(stdstaff_id,stdfname,stdsname,stdoname,stdgender,stdsupervisor,stdemail,stdrole,stddepartment,stdposition,stdgrade);
return 'inserted successfully';
	   end;
$$;


--
-- Name: start_date(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.start_date() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	
		 INSERT INTO "yearly_details"("year")
		 VALUES(new."year");

	RETURN NEW;
END;
$$;


--
-- Name: training_recieved(integer, character varying, character varying, date, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.training_recieved(stdtraining_recieved_id integer, stdinstitution character varying, stdprogramme character varying, stddate date, stdappraisalid integer) RETURNS character varying
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
    appraisal_id integer NOT NULL,
    status character varying NOT NULL,
    annual_appraisal_id integer NOT NULL
);


--
-- Name: annual_plan ; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."annual_plan " (
    result_areas character varying NOT NULL,
    target character varying NOT NULL,
    resources character varying NOT NULL,
    appraisal_id integer NOT NULL,
    annual_plan_id integer NOT NULL,
    status integer NOT NULL,
    form_hash character varying NOT NULL
);


--
-- Name: appraisal_form; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.appraisal_form (
    department character varying NOT NULL,
    grade integer NOT NULL,
    "position" character varying NOT NULL,
    appraisal_form_id integer NOT NULL,
    date date NOT NULL,
    staff_id integer NOT NULL
);


--
-- Name: competency; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.competency (
    category character varying NOT NULL,
    weight integer NOT NULL,
    sub integer NOT NULL,
    main character varying NOT NULL,
    competency_id integer NOT NULL,
    appraisal_id integer NOT NULL
);


--
-- Name: deadline; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.deadline (
    type character varying NOT NULL,
    start_date date NOT NULL,
    ending date NOT NULL,
    deadline_id integer NOT NULL
);


--
-- Name: endofyear_review; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.endofyear_review (
    assessment character varying,
    score integer,
    comment character varying,
    appraisal_id integer,
    endofyear_review_id integer,
    annual_plan_id integer,
    weight integer,
    status integer
);


--
-- Name: form_completion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.form_completion (
    form_completion_id integer,
    appraisal_id integer,
    date date,
    status integer
);


--
-- Name: hash_table; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hash_table (
    hash character varying(1000) NOT NULL,
    email character varying,
    hash_table_id integer NOT NULL
);


--
-- Name: logIn; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."logIn" (
    staff_id integer NOT NULL,
    username character varying NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL,
    login_id integer NOT NULL
);


--
-- Name: midyear_review; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.midyear_review (
    midyear_review_id integer NOT NULL,
    progress_review character varying NOT NULL,
    remarks character varying NOT NULL,
    status integer NOT NULL,
    appraisal_id integer NOT NULL,
    annual_plan_id integer NOT NULL
);


--
-- Name: staff; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.staff (
    staff_id integer NOT NULL,
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
-- Name: training_recieved; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.training_recieved (
    training_recieved_id integer NOT NULL,
    institution character varying NOT NULL,
    programme character varying NOT NULL,
    date date NOT NULL,
    appraisal_id integer NOT NULL
);


--
-- Name: yearly_details; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.yearly_details (
    department character varying,
    grade integer,
    "position" character varying,
    year date,
    staff_id integer
);


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
-- Data for Name: hash_table; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: logIn; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: midyear_review; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: staff; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: training_recieved; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: yearly_details; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Name: annual_plan  ann_plan_uq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."annual_plan "
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
-- Name: annual_plan  annual_plan _pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."annual_plan "
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
-- Name: staff email_insert_trigger; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER email_insert_trigger AFTER INSERT OR UPDATE ON public.staff FOR EACH ROW EXECUTE FUNCTION public.email_insert_trigger_fnc();


--
-- Name: hash_table hash_insert_trigger; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER hash_insert_trigger AFTER INSERT ON public.hash_table FOR EACH ROW EXECUTE FUNCTION public.hash_insert_trigger_fnc();


--
-- Name: annual_plan  start_date_trigger; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER start_date_trigger AFTER INSERT OR UPDATE ON public."annual_plan " FOR EACH ROW EXECUTE FUNCTION public.start_date();


--
-- Name: staff yearly_details; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER yearly_details AFTER INSERT ON public.staff FOR EACH ROW EXECUTE FUNCTION public.yearly_details();


--
-- Name: annual_appraisal ann_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.annual_appraisal
    ADD CONSTRAINT ann_fk FOREIGN KEY (appraisal_id) REFERENCES public.appraisal_form(appraisal_form_id) NOT VALID;


--
-- Name: annual_plan  ann_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."annual_plan "
    ADD CONSTRAINT ann_fk FOREIGN KEY (appraisal_id) REFERENCES public.appraisal_form(appraisal_form_id) NOT VALID;


--
-- Name: appraisal_form app_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appraisal_form
    ADD CONSTRAINT app_fk FOREIGN KEY (staff_id) REFERENCES public.staff(staff_id) NOT VALID;


--
-- Name: endofyear_review end_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.endofyear_review
    ADD CONSTRAINT end_fk FOREIGN KEY (appraisal_id) REFERENCES public.appraisal_form(appraisal_form_id) NOT VALID;


--
-- Name: endofyear_review end_fk_2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.endofyear_review
    ADD CONSTRAINT end_fk_2 FOREIGN KEY (annual_plan_id) REFERENCES public."annual_plan "(annual_plan_id) NOT VALID;


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
    ADD CONSTRAINT mid2_fk FOREIGN KEY (appraisal_id) REFERENCES public.appraisal_form(appraisal_form_id) NOT VALID;


--
-- Name: midyear_review mid_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.midyear_review
    ADD CONSTRAINT mid_fk FOREIGN KEY (annual_plan_id) REFERENCES public."annual_plan "(annual_plan_id) NOT VALID;


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

