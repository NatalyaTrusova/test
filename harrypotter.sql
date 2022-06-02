--
-- PostgreSQL database dump
--

-- Dumped from database version 12.9
-- Dumped by pg_dump version 12.9

-- Started on 2022-03-27 15:45:50

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
-- TOC entry 203 (class 1259 OID 17125)
-- Name: heroes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.heroes (
    id integer NOT NULL,
    name character varying(30) NOT NULL,
    birthday timestamp with time zone NOT NULL,
    side character varying(30) NOT NULL,
    power integer,
    update_dttm timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.heroes OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 17123)
-- Name: heroes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.heroes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.heroes_id_seq OWNER TO postgres;

--
-- TOC entry 2878 (class 0 OID 0)
-- Dependencies: 202
-- Name: heroes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.heroes_id_seq OWNED BY public.heroes.id;


--
-- TOC entry 207 (class 1259 OID 17143)
-- Name: heroes_warfares; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.heroes_warfares (
    id integer NOT NULL,
    hero_id integer NOT NULL,
    warfare_id integer NOT NULL
);


ALTER TABLE public.heroes_warfares OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 17141)
-- Name: heroes_warfares_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.heroes_warfares_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.heroes_warfares_id_seq OWNER TO postgres;

--
-- TOC entry 2879 (class 0 OID 0)
-- Dependencies: 206
-- Name: heroes_warfares_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.heroes_warfares_id_seq OWNED BY public.heroes_warfares.id;


--
-- TOC entry 209 (class 1259 OID 17162)
-- Name: slogans; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.slogans (
    id integer NOT NULL,
    hero_id integer NOT NULL,
    moto text NOT NULL,
    moto_id integer NOT NULL
);


ALTER TABLE public.slogans OWNER TO postgres;

--
-- TOC entry 208 (class 1259 OID 17160)
-- Name: slogans_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.slogans_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.slogans_id_seq OWNER TO postgres;

--
-- TOC entry 2880 (class 0 OID 0)
-- Dependencies: 208
-- Name: slogans_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.slogans_id_seq OWNED BY public.slogans.id;


--
-- TOC entry 211 (class 1259 OID 17178)
-- Name: stories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stories (
    id integer NOT NULL,
    story text NOT NULL,
    hero_id integer NOT NULL
);


ALTER TABLE public.stories OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 17176)
-- Name: stories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.stories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.stories_id_seq OWNER TO postgres;

--
-- TOC entry 2881 (class 0 OID 0)
-- Dependencies: 210
-- Name: stories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.stories_id_seq OWNED BY public.stories.id;


--
-- TOC entry 205 (class 1259 OID 17134)
-- Name: warfares; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.warfares (
    id integer NOT NULL,
    hero_1_id integer NOT NULL,
    hero_1_moto_id integer,
    hero_2_id integer NOT NULL,
    hero_2_moto_id integer,
    winner integer,
    CONSTRAINT warfares_winner_check CHECK ((winner = ANY (ARRAY[NULL::integer, 1, 2])))
);


ALTER TABLE public.warfares OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 17132)
-- Name: warfares_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.warfares_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.warfares_id_seq OWNER TO postgres;

--
-- TOC entry 2882 (class 0 OID 0)
-- Dependencies: 204
-- Name: warfares_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.warfares_id_seq OWNED BY public.warfares.id;


--
-- TOC entry 2713 (class 2604 OID 17128)
-- Name: heroes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.heroes ALTER COLUMN id SET DEFAULT nextval('public.heroes_id_seq'::regclass);


--
-- TOC entry 2717 (class 2604 OID 17146)
-- Name: heroes_warfares id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.heroes_warfares ALTER COLUMN id SET DEFAULT nextval('public.heroes_warfares_id_seq'::regclass);


--
-- TOC entry 2718 (class 2604 OID 17165)
-- Name: slogans id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.slogans ALTER COLUMN id SET DEFAULT nextval('public.slogans_id_seq'::regclass);


--
-- TOC entry 2719 (class 2604 OID 17181)
-- Name: stories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stories ALTER COLUMN id SET DEFAULT nextval('public.stories_id_seq'::regclass);


--
-- TOC entry 2715 (class 2604 OID 17137)
-- Name: warfares id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.warfares ALTER COLUMN id SET DEFAULT nextval('public.warfares_id_seq'::regclass);


--
-- TOC entry 2864 (class 0 OID 17125)
-- Dependencies: 203
-- Data for Name: heroes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.heroes (id, name, birthday, side, power, update_dttm) FROM stdin;
1	Harry Potter	1980-07-31 00:00:00+03	Phoenix Order	100	2022-03-26 21:28:44.273262+03
2	Bellatrix Lestrange	1951-02-15 00:00:00+03	Death Eaters	90	2022-03-26 21:28:44.282362+03
3	Sirius Black	1961-02-15 00:00:00+03	Phoenix Order	85	2022-03-26 21:28:44.28703+03
4	Lucius Malfoy	1941-03-12 00:00:00+03	Death Eaters	80	2022-03-26 21:28:44.290494+03
5	Ron Weasley	1981-03-14 00:00:00+03	Phoenix Order	99	2022-03-26 21:28:44.294045+03
6	Draco Malfoy	1980-10-30 00:00:00+03	Death Eaters	\N	2022-03-26 21:28:44.29717+03
\.


--
-- TOC entry 2868 (class 0 OID 17143)
-- Dependencies: 207
-- Data for Name: heroes_warfares; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.heroes_warfares (id, hero_id, warfare_id) FROM stdin;
\.


--
-- TOC entry 2870 (class 0 OID 17162)
-- Dependencies: 209
-- Data for Name: slogans; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.slogans (id, hero_id, moto, moto_id) FROM stdin;
1	1	But I'm Harry... Just a Harry!	1
2	2	I've killed Sirius Black!	1
3	3	Each has both a white and a black side.	1
\.


--
-- TOC entry 2872 (class 0 OID 17178)
-- Dependencies: 211
-- Data for Name: stories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stories (id, story, hero_id) FROM stdin;
1	First survived Avada Kedavra. His parents were killed then he was a little boy.	1
2	Death Eater, Voldemort's most zealous henchman.	2
\.


--
-- TOC entry 2866 (class 0 OID 17134)
-- Dependencies: 205
-- Data for Name: warfares; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.warfares (id, hero_1_id, hero_1_moto_id, hero_2_id, hero_2_moto_id, winner) FROM stdin;
1	6	\N	1	1	\N
2	3	3	7	4	1
3	6	\N	7	4	\N
4	3	3	4	\N	1
5	1	1	5	\N	\N
\.


--
-- TOC entry 2883 (class 0 OID 0)
-- Dependencies: 202
-- Name: heroes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.heroes_id_seq', 7, true);


--
-- TOC entry 2884 (class 0 OID 0)
-- Dependencies: 206
-- Name: heroes_warfares_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.heroes_warfares_id_seq', 1, false);


--
-- TOC entry 2885 (class 0 OID 0)
-- Dependencies: 208
-- Name: slogans_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.slogans_id_seq', 4, true);


--
-- TOC entry 2886 (class 0 OID 0)
-- Dependencies: 210
-- Name: stories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.stories_id_seq', 2, true);


--
-- TOC entry 2887 (class 0 OID 0)
-- Dependencies: 204
-- Name: warfares_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.warfares_id_seq', 5, true);


--
-- TOC entry 2721 (class 2606 OID 17131)
-- Name: heroes heroes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.heroes
    ADD CONSTRAINT heroes_pkey PRIMARY KEY (id);


--
-- TOC entry 2725 (class 2606 OID 17148)
-- Name: heroes_warfares heroes_warfares_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.heroes_warfares
    ADD CONSTRAINT heroes_warfares_pkey PRIMARY KEY (id);


--
-- TOC entry 2728 (class 2606 OID 17170)
-- Name: slogans slogans_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.slogans
    ADD CONSTRAINT slogans_pkey PRIMARY KEY (id);


--
-- TOC entry 2730 (class 2606 OID 17188)
-- Name: stories stories_hero_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stories
    ADD CONSTRAINT stories_hero_id_key UNIQUE (hero_id);


--
-- TOC entry 2732 (class 2606 OID 17186)
-- Name: stories stories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stories
    ADD CONSTRAINT stories_pkey PRIMARY KEY (id);


--
-- TOC entry 2723 (class 2606 OID 17140)
-- Name: warfares warfares_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.warfares
    ADD CONSTRAINT warfares_pkey PRIMARY KEY (id);


--
-- TOC entry 2726 (class 1259 OID 17159)
-- Name: ix_heroes_warfares_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_heroes_warfares_id ON public.heroes_warfares USING btree (id);


--
-- TOC entry 2733 (class 2606 OID 17149)
-- Name: heroes_warfares heroes_warfares_hero_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.heroes_warfares
    ADD CONSTRAINT heroes_warfares_hero_id_fkey FOREIGN KEY (hero_id) REFERENCES public.heroes(id);


--
-- TOC entry 2734 (class 2606 OID 17154)
-- Name: heroes_warfares heroes_warfares_warfare_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.heroes_warfares
    ADD CONSTRAINT heroes_warfares_warfare_id_fkey FOREIGN KEY (warfare_id) REFERENCES public.warfares(id);


--
-- TOC entry 2735 (class 2606 OID 17171)
-- Name: slogans slogans_hero_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.slogans
    ADD CONSTRAINT slogans_hero_id_fkey FOREIGN KEY (hero_id) REFERENCES public.heroes(id) ON DELETE CASCADE;


--
-- TOC entry 2736 (class 2606 OID 17189)
-- Name: stories stories_hero_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stories
    ADD CONSTRAINT stories_hero_id_fkey FOREIGN KEY (hero_id) REFERENCES public.heroes(id) ON DELETE CASCADE;


-- Completed on 2022-03-27 15:45:50

--
-- PostgreSQL database dump complete
--

