--
-- PostgreSQL database dump
--

-- Dumped from database version 13.4
-- Dumped by pg_dump version 13.4

-- THIS FILE IS INCLUDED FOR DOCUMENTATION PURPOSES ONLY
-- THE ACTUAL DDL IS PERFORMED BY ALEMBIC 
-- See scripts in alembic/versions

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: activities; Type: TABLE; Schema: public; Owner: ptuomola
--

CREATE TABLE public.activities (
    id integer NOT NULL,
    description character varying NOT NULL,
    activity_type integer NOT NULL
);


ALTER TABLE public.activities OWNER TO ptuomola;

--
-- Name: activities_id_seq; Type: SEQUENCE; Schema: public; Owner: ptuomola
--

CREATE SEQUENCE public.activities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.activities_id_seq OWNER TO ptuomola;

--
-- Name: activities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ptuomola
--

ALTER SEQUENCE public.activities_id_seq OWNED BY public.activities.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: ptuomola
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO ptuomola;

--
-- Name: exercise_subactivities; Type: TABLE; Schema: public; Owner: ptuomola
--

CREATE TABLE public.exercise_subactivities (
    id integer NOT NULL,
    exercise_id integer NOT NULL,
    subactivity_id integer NOT NULL,
    count integer
);


ALTER TABLE public.exercise_subactivities OWNER TO ptuomola;

--
-- Name: exercise_subactivities_id_seq; Type: SEQUENCE; Schema: public; Owner: ptuomola
--

CREATE SEQUENCE public.exercise_subactivities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exercise_subactivities_id_seq OWNER TO ptuomola;

--
-- Name: exercise_subactivities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ptuomola
--

ALTER SEQUENCE public.exercise_subactivities_id_seq OWNED BY public.exercise_subactivities.id;


--
-- Name: exercises; Type: TABLE; Schema: public; Owner: ptuomola
--

CREATE TABLE public.exercises (
    id integer NOT NULL,
    user_id integer NOT NULL,
    start_date date NOT NULL,
    start_time time without time zone,
    end_date date,
    end_time time without time zone,
    description character varying,
    external_url character varying,
    activity_id integer NOT NULL
);


ALTER TABLE public.exercises OWNER TO ptuomola;

--
-- Name: exercises_id_seq; Type: SEQUENCE; Schema: public; Owner: ptuomola
--

CREATE SEQUENCE public.exercises_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.exercises_id_seq OWNER TO ptuomola;

--
-- Name: exercises_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ptuomola
--

ALTER SEQUENCE public.exercises_id_seq OWNED BY public.exercises.id;


--
-- Name: subactivities; Type: TABLE; Schema: public; Owner: ptuomola
--

CREATE TABLE public.subactivities (
    id integer NOT NULL,
    activity_id integer NOT NULL,
    description character varying NOT NULL
);


ALTER TABLE public.subactivities OWNER TO ptuomola;

--
-- Name: subactivities_id_seq; Type: SEQUENCE; Schema: public; Owner: ptuomola
--

CREATE SEQUENCE public.subactivities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subactivities_id_seq OWNER TO ptuomola;

--
-- Name: subactivities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ptuomola
--

ALTER SEQUENCE public.subactivities_id_seq OWNED BY public.subactivities.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: ptuomola
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL,
    name character varying,
    superuser boolean DEFAULT false
);


ALTER TABLE public.users OWNER TO ptuomola;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: ptuomola
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO ptuomola;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ptuomola
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: activities id; Type: DEFAULT; Schema: public; Owner: ptuomola
--

ALTER TABLE ONLY public.activities ALTER COLUMN id SET DEFAULT nextval('public.activities_id_seq'::regclass);


--
-- Name: exercise_subactivities id; Type: DEFAULT; Schema: public; Owner: ptuomola
--

ALTER TABLE ONLY public.exercise_subactivities ALTER COLUMN id SET DEFAULT nextval('public.exercise_subactivities_id_seq'::regclass);


--
-- Name: exercises id; Type: DEFAULT; Schema: public; Owner: ptuomola
--

ALTER TABLE ONLY public.exercises ALTER COLUMN id SET DEFAULT nextval('public.exercises_id_seq'::regclass);


--
-- Name: subactivities id; Type: DEFAULT; Schema: public; Owner: ptuomola
--

ALTER TABLE ONLY public.subactivities ALTER COLUMN id SET DEFAULT nextval('public.subactivities_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: ptuomola
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: activities activities_pkey; Type: CONSTRAINT; Schema: public; Owner: ptuomola
--

ALTER TABLE ONLY public.activities
    ADD CONSTRAINT activities_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: ptuomola
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: exercise_subactivities exercise_subactivities_pkey; Type: CONSTRAINT; Schema: public; Owner: ptuomola
--

ALTER TABLE ONLY public.exercise_subactivities
    ADD CONSTRAINT exercise_subactivities_pkey PRIMARY KEY (id);


--
-- Name: exercises exercises_pkey; Type: CONSTRAINT; Schema: public; Owner: ptuomola
--

ALTER TABLE ONLY public.exercises
    ADD CONSTRAINT exercises_pkey PRIMARY KEY (id);


--
-- Name: subactivities subactivities_pkey; Type: CONSTRAINT; Schema: public; Owner: ptuomola
--

ALTER TABLE ONLY public.subactivities
    ADD CONSTRAINT subactivities_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: ptuomola
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: exercise_subactivities exercise_subactivities_exercise_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ptuomola
--

ALTER TABLE ONLY public.exercise_subactivities
    ADD CONSTRAINT exercise_subactivities_exercise_id_fkey FOREIGN KEY (exercise_id) REFERENCES public.exercises(id) ON DELETE CASCADE;


--
-- Name: exercise_subactivities exercise_subactivities_subactivity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ptuomola
--

ALTER TABLE ONLY public.exercise_subactivities
    ADD CONSTRAINT exercise_subactivities_subactivity_id_fkey FOREIGN KEY (subactivity_id) REFERENCES public.subactivities(id) ON DELETE CASCADE;


--
-- Name: exercises fk_activity_id; Type: FK CONSTRAINT; Schema: public; Owner: ptuomola
--

ALTER TABLE ONLY public.exercises
    ADD CONSTRAINT fk_activity_id FOREIGN KEY (activity_id) REFERENCES public.activities(id);


--
-- Name: subactivities fk_activity_id; Type: FK CONSTRAINT; Schema: public; Owner: ptuomola
--

ALTER TABLE ONLY public.subactivities
    ADD CONSTRAINT fk_activity_id FOREIGN KEY (activity_id) REFERENCES public.activities(id) ON DELETE CASCADE;


--
-- Name: exercises fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: ptuomola
--

ALTER TABLE ONLY public.exercises
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: subactivities subactivities_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ptuomola
--

ALTER TABLE ONLY public.subactivities
    ADD CONSTRAINT subactivities_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES public.activities(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

