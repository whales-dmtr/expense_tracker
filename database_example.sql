--
-- PostgreSQL database dump
--

-- Dumped from database version 14.18 (Homebrew)
-- Dumped by pg_dump version 14.18 (Homebrew)

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
-- Name: expenses; Type: TABLE; Schema: public; Owner: dima
--

CREATE TABLE public.expenses (
    id integer NOT NULL,
    description character varying(50) NOT NULL,
    amount numeric(10,2) NOT NULL,
    time_created timestamp without time zone NOT NULL,
    category character varying(11) NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.expenses OWNER TO dima;

--
-- Name: users; Type: TABLE; Schema: public; Owner: dima
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(15) NOT NULL,
    password character varying NOT NULL,
    email character varying NOT NULL
);


ALTER TABLE public.users OWNER TO dima;

--
-- Name: expenses_id_seq; Type: SEQUENCE; Schema: public; Owner: dima
--

CREATE SEQUENCE public.expenses_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.expenses_id_seq OWNER TO dima;

--
-- Name: expenses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dima
--

ALTER SEQUENCE public.expenses_id_seq OWNED BY public.users.id;


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: dima
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO dima;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dima
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Data for Name: expenses; Type: TABLE DATA; Schema: public; Owner: dima
--

COPY public.expenses (id, description, amount, time_created, category, user_id) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: dima
--

COPY public.users (id, username, password, email) FROM stdin;
\.


--
-- Name: expenses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dima
--

SELECT pg_catalog.setval('public.expenses_id_seq', 5, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dima
--

SELECT pg_catalog.setval('public.users_id_seq', 72, true);


--
-- Name: expenses expenses_pkey; Type: CONSTRAINT; Schema: public; Owner: dima
--

ALTER TABLE ONLY public.expenses
    ADD CONSTRAINT expenses_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: dima
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: dima
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: dima
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: expenses users_id_pk; Type: FK CONSTRAINT; Schema: public; Owner: dima
--

ALTER TABLE ONLY public.expenses
    ADD CONSTRAINT users_id_pk FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

