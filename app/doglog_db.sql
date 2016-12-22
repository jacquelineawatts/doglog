--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.1
-- Dumped by pg_dump version 9.6.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: activities; Type: TABLE; Schema: public; Owner: jacqui
--

CREATE TABLE activities (
    activity_id integer NOT NULL,
    activity character varying(30),
    min_daily integer,
    max_daily integer
);


ALTER TABLE activities OWNER TO jacqui;

--
-- Name: activities_activity_id_seq; Type: SEQUENCE; Schema: public; Owner: jacqui
--

CREATE SEQUENCE activities_activity_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE activities_activity_id_seq OWNER TO jacqui;

--
-- Name: activities_activity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jacqui
--

ALTER SEQUENCE activities_activity_id_seq OWNED BY activities.activity_id;


--
-- Name: entries; Type: TABLE; Schema: public; Owner: jacqui
--

CREATE TABLE entries (
    entry_id integer NOT NULL,
    user_id integer NOT NULL,
    pet_id integer NOT NULL,
    activity_id integer NOT NULL,
    occurred_at timestamp without time zone NOT NULL,
    logged_at timestamp without time zone NOT NULL,
    notes text
);


ALTER TABLE entries OWNER TO jacqui;

--
-- Name: entries_entry_id_seq; Type: SEQUENCE; Schema: public; Owner: jacqui
--

CREATE SEQUENCE entries_entry_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE entries_entry_id_seq OWNER TO jacqui;

--
-- Name: entries_entry_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jacqui
--

ALTER SEQUENCE entries_entry_id_seq OWNED BY entries.entry_id;


--
-- Name: pets; Type: TABLE; Schema: public; Owner: jacqui
--

CREATE TABLE pets (
    pet_id integer NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    animal character varying(30) NOT NULL,
    breed character varying(30),
    birthdate timestamp without time zone NOT NULL,
    bio text,
    profile_img character varying(256)
);


ALTER TABLE pets OWNER TO jacqui;

--
-- Name: pets_pet_id_seq; Type: SEQUENCE; Schema: public; Owner: jacqui
--

CREATE SEQUENCE pets_pet_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE pets_pet_id_seq OWNER TO jacqui;

--
-- Name: pets_pet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jacqui
--

ALTER SEQUENCE pets_pet_id_seq OWNED BY pets.pet_id;


--
-- Name: pets_users; Type: TABLE; Schema: public; Owner: jacqui
--

CREATE TABLE pets_users (
    petuser_id integer NOT NULL,
    user_id integer NOT NULL,
    pet_id integer NOT NULL,
    role character varying(30) NOT NULL
);


ALTER TABLE pets_users OWNER TO jacqui;

--
-- Name: pets_users_petuser_id_seq; Type: SEQUENCE; Schema: public; Owner: jacqui
--

CREATE SEQUENCE pets_users_petuser_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE pets_users_petuser_id_seq OWNER TO jacqui;

--
-- Name: pets_users_petuser_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jacqui
--

ALTER SEQUENCE pets_users_petuser_id_seq OWNED BY pets_users.petuser_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: jacqui
--

CREATE TABLE users (
    user_id integer NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    username character varying(30) NOT NULL,
    email character varying(64) NOT NULL,
    password character varying(64) NOT NULL,
    profile_img character varying(256),
    created_at timestamp without time zone
);


ALTER TABLE users OWNER TO jacqui;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: jacqui
--

CREATE SEQUENCE users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_user_id_seq OWNER TO jacqui;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jacqui
--

ALTER SEQUENCE users_user_id_seq OWNED BY users.user_id;


--
-- Name: activities activity_id; Type: DEFAULT; Schema: public; Owner: jacqui
--

ALTER TABLE ONLY activities ALTER COLUMN activity_id SET DEFAULT nextval('activities_activity_id_seq'::regclass);


--
-- Name: entries entry_id; Type: DEFAULT; Schema: public; Owner: jacqui
--

ALTER TABLE ONLY entries ALTER COLUMN entry_id SET DEFAULT nextval('entries_entry_id_seq'::regclass);


--
-- Name: pets pet_id; Type: DEFAULT; Schema: public; Owner: jacqui
--

ALTER TABLE ONLY pets ALTER COLUMN pet_id SET DEFAULT nextval('pets_pet_id_seq'::regclass);


--
-- Name: pets_users petuser_id; Type: DEFAULT; Schema: public; Owner: jacqui
--

ALTER TABLE ONLY pets_users ALTER COLUMN petuser_id SET DEFAULT nextval('pets_users_petuser_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: jacqui
--

ALTER TABLE ONLY users ALTER COLUMN user_id SET DEFAULT nextval('users_user_id_seq'::regclass);


--
-- Data for Name: activities; Type: TABLE DATA; Schema: public; Owner: jacqui
--

COPY activities (activity_id, activity, min_daily, max_daily) FROM stdin;
1	#1	\N	\N
2	#2	\N	\N
3	food	1	2
4	walk	\N	\N
\.


--
-- Name: activities_activity_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jacqui
--

SELECT pg_catalog.setval('activities_activity_id_seq', 4, true);


--
-- Data for Name: entries; Type: TABLE DATA; Schema: public; Owner: jacqui
--

COPY entries (entry_id, user_id, pet_id, activity_id, occurred_at, logged_at, notes) FROM stdin;
\.


--
-- Name: entries_entry_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jacqui
--

SELECT pg_catalog.setval('entries_entry_id_seq', 1, false);


--
-- Data for Name: pets; Type: TABLE DATA; Schema: public; Owner: jacqui
--

COPY pets (pet_id, first_name, last_name, animal, breed, birthdate, bio, profile_img) FROM stdin;
1	Zoe	Watts	dog	dachshund	2012-01-01 00:00:00	\N	\N
2	Cali	Watts	cat	calico	2008-01-01 00:00:00	\N	\N
\.


--
-- Name: pets_pet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jacqui
--

SELECT pg_catalog.setval('pets_pet_id_seq', 2, true);


--
-- Data for Name: pets_users; Type: TABLE DATA; Schema: public; Owner: jacqui
--

COPY pets_users (petuser_id, user_id, pet_id, role) FROM stdin;
1	1	1	secondary
2	2	1	primary
3	1	2	secondary
4	2	2	primary
\.


--
-- Name: pets_users_petuser_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jacqui
--

SELECT pg_catalog.setval('pets_users_petuser_id_seq', 4, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: jacqui
--

COPY users (user_id, first_name, last_name, username, email, password, profile_img, created_at) FROM stdin;
1	Jacqui	Watts	jacquelineawatts	jacqui@test.org	test	\N	\N
2	Pam	Watts	pamrwatts	pam@test.org	test	\N	\N
\.


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jacqui
--

SELECT pg_catalog.setval('users_user_id_seq', 2, true);


--
-- Name: activities activities_pkey; Type: CONSTRAINT; Schema: public; Owner: jacqui
--

ALTER TABLE ONLY activities
    ADD CONSTRAINT activities_pkey PRIMARY KEY (activity_id);


--
-- Name: entries entries_pkey; Type: CONSTRAINT; Schema: public; Owner: jacqui
--

ALTER TABLE ONLY entries
    ADD CONSTRAINT entries_pkey PRIMARY KEY (entry_id);


--
-- Name: pets pets_pkey; Type: CONSTRAINT; Schema: public; Owner: jacqui
--

ALTER TABLE ONLY pets
    ADD CONSTRAINT pets_pkey PRIMARY KEY (pet_id);


--
-- Name: pets_users pets_users_pkey; Type: CONSTRAINT; Schema: public; Owner: jacqui
--

ALTER TABLE ONLY pets_users
    ADD CONSTRAINT pets_users_pkey PRIMARY KEY (petuser_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: jacqui
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: jacqui
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: entries entries_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jacqui
--

ALTER TABLE ONLY entries
    ADD CONSTRAINT entries_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES activities(activity_id);


--
-- Name: entries entries_pet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jacqui
--

ALTER TABLE ONLY entries
    ADD CONSTRAINT entries_pet_id_fkey FOREIGN KEY (pet_id) REFERENCES pets(pet_id);


--
-- Name: entries entries_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jacqui
--

ALTER TABLE ONLY entries
    ADD CONSTRAINT entries_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: pets_users pets_users_pet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jacqui
--

ALTER TABLE ONLY pets_users
    ADD CONSTRAINT pets_users_pet_id_fkey FOREIGN KEY (pet_id) REFERENCES pets(pet_id);


--
-- Name: pets_users pets_users_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jacqui
--

ALTER TABLE ONLY pets_users
    ADD CONSTRAINT pets_users_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- PostgreSQL database dump complete
--

