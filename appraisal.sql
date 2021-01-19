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
        done := NOT exists(SELECT 1 FROM staff WHERE Email=new_hash);
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
select * into annual_appraisal_details from annual_appraisal;
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
select * into annual_plan_details from annual_plan;
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
select * into appraisal_form_details from appraisal_form;
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
select * into competency_details  from competency;
return competency_details ;
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
select * into endofyear_review_detals  from endofyear_review;
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
select * into form_detals  from form_completion;
return form_detals  ;
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
select * into midyear_review_detals  from midyear_review;
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
select * into staff_details from staff  ;
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
select * into training_recieved_details  from training_recieved;
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
-- Name: staff(character varying, character varying, character varying, character varying, character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.staff(stdid character varying, stdfname character varying, stdsname character varying, stdoname character varying, stdgender character varying, stdsupervisor character varying, stdemail character varying) RETURNS character varying
    LANGUAGE plpgsql
    AS $$
declare
begin
insert into public.Staff(ID,Fname,Sname,Oname,Gender,Supervisor,Email)
values(stdID,stdFname,stdSname,stdOname,stdGender,stdSupervisor,stdEmail);
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
    hash character varying(1000) DEFAULT public.generate_hash()
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
    "ID" integer NOT NULL,
    "Fname" character varying NOT NULL,
    "Sname" character varying NOT NULL,
    "Oname" character varying NOT NULL,
    "Gender" character varying NOT NULL,
    "Supervisor" character varying NOT NULL,
    "Email" character varying
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
-- Data for Name: endofyear_review; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: form_completion; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: hash; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.hash (hash) VALUES (NULL);
INSERT INTO public.hash (hash) VALUES (NULL);
INSERT INTO public.hash (hash) VALUES ('$$');
INSERT INTO public.hash (hash) VALUES ('LJrtLTVIqGH41STaKKaJ');
INSERT INTO public.hash (hash) VALUES ('FDkAiCprTjvZUDt9PgYw');


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



--
-- Data for Name: training_recieved; Type: TABLE DATA; Schema: public; Owner: -
--



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
    ADD CONSTRAINT "Staff_id" UNIQUE ("ID");


--
-- Name: staff Staff_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT "Staff_pkey" PRIMARY KEY ("ID");


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
-- Name: form_completion form_completion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.form_completion
    ADD CONSTRAINT form_completion_pkey PRIMARY KEY ("ID");


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
-- Name: quickaccess EFK; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.quickaccess
    ADD CONSTRAINT "EFK" FOREIGN KEY (email) REFERENCES public.staff("Email") NOT VALID;


--
-- Name: logIn Staff ID; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."logIn"
    ADD CONSTRAINT "Staff ID" FOREIGN KEY ("StaffID") REFERENCES public.staff("ID") NOT VALID;


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
    ADD CONSTRAINT appstaffid FOREIGN KEY ("StaffID") REFERENCES public.staff("ID") NOT VALID;


--
-- Name: competency comFK; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.competency
    ADD CONSTRAINT "comFK" FOREIGN KEY ("AppraisalID") REFERENCES public.appraisal_form("ID") NOT VALID;


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

