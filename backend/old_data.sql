--
-- PostgreSQL database dump
--

\restrict Yit6JLX3ZQprhRdJiBrXV8aSMg1nB29xCGTeYdKbEBgeFhtmcoeTB23qmMtJtTW

-- Dumped from database version 14.19 (Homebrew)
-- Dumped by pg_dump version 14.19 (Homebrew)

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
-- Name: contactstatusenum; Type: TYPE; Schema: public; Owner: mailforge_user
--

CREATE TYPE public.contactstatusenum AS ENUM (
    'valid',
    'invalid'
);


ALTER TYPE public.contactstatusenum OWNER TO mailforge_user;

--
-- Name: messagestatusenum; Type: TYPE; Schema: public; Owner: mailforge_user
--

CREATE TYPE public.messagestatusenum AS ENUM (
    'queued',
    'sent'
);


ALTER TYPE public.messagestatusenum OWNER TO mailforge_user;

--
-- Name: roleenum; Type: TYPE; Schema: public; Owner: mailforge_user
--

CREATE TYPE public.roleenum AS ENUM (
    'owner',
    'member'
);


ALTER TYPE public.roleenum OWNER TO mailforge_user;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: mailforge_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO mailforge_user;

--
-- Name: blacklisted_tokens; Type: TABLE; Schema: public; Owner: mailforge_user
--

CREATE TABLE public.blacklisted_tokens (
    id integer NOT NULL,
    token character varying(512) NOT NULL,
    expires_at timestamp without time zone NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.blacklisted_tokens OWNER TO mailforge_user;

--
-- Name: blacklisted_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: mailforge_user
--

CREATE SEQUENCE public.blacklisted_tokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.blacklisted_tokens_id_seq OWNER TO mailforge_user;

--
-- Name: blacklisted_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mailforge_user
--

ALTER SEQUENCE public.blacklisted_tokens_id_seq OWNED BY public.blacklisted_tokens.id;


--
-- Name: campaign_batches; Type: TABLE; Schema: public; Owner: mailforge_user
--

CREATE TABLE public.campaign_batches (
    id integer NOT NULL,
    campaign_id integer,
    status character varying(50),
    sent_at timestamp without time zone,
    meta json,
    batch_index integer NOT NULL
);


ALTER TABLE public.campaign_batches OWNER TO mailforge_user;

--
-- Name: campaign_batches_id_seq; Type: SEQUENCE; Schema: public; Owner: mailforge_user
--

CREATE SEQUENCE public.campaign_batches_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.campaign_batches_id_seq OWNER TO mailforge_user;

--
-- Name: campaign_batches_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mailforge_user
--

ALTER SEQUENCE public.campaign_batches_id_seq OWNED BY public.campaign_batches.id;


--
-- Name: campaigns; Type: TABLE; Schema: public; Owner: mailforge_user
--

CREATE TABLE public.campaigns (
    id integer NOT NULL,
    tenant_id integer,
    name character varying(255) NOT NULL,
    subject character varying(512),
    body text,
    sender character varying(255),
    status character varying(50),
    ai_score double precision,
    ai_suggestions json,
    created_at timestamp without time zone,
    query json,
    local_kw json,
    recheck_every_batches integer,
    recheck_every_minutes integer,
    max_consecutive_spam integer,
    show_badge boolean
);


ALTER TABLE public.campaigns OWNER TO mailforge_user;

--
-- Name: campaigns_id_seq; Type: SEQUENCE; Schema: public; Owner: mailforge_user
--

CREATE SEQUENCE public.campaigns_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.campaigns_id_seq OWNER TO mailforge_user;

--
-- Name: campaigns_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mailforge_user
--

ALTER SEQUENCE public.campaigns_id_seq OWNED BY public.campaigns.id;


--
-- Name: message_logs; Type: TABLE; Schema: public; Owner: mailforge_user
--

CREATE TABLE public.message_logs (
    id integer NOT NULL,
    tenant_id integer,
    campaign_id integer,
    recipient character varying(320),
    smtp_id integer,
    status character varying(50),
    details json,
    created_at timestamp without time zone
);


ALTER TABLE public.message_logs OWNER TO mailforge_user;

--
-- Name: message_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: mailforge_user
--

CREATE SEQUENCE public.message_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.message_logs_id_seq OWNER TO mailforge_user;

--
-- Name: message_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mailforge_user
--

ALTER SEQUENCE public.message_logs_id_seq OWNED BY public.message_logs.id;


--
-- Name: password_reset_tokens; Type: TABLE; Schema: public; Owner: mailforge_user
--

CREATE TABLE public.password_reset_tokens (
    id integer NOT NULL,
    user_id integer NOT NULL,
    token_hash character varying NOT NULL,
    expires_at timestamp without time zone NOT NULL,
    used boolean,
    created_at timestamp without time zone
);


ALTER TABLE public.password_reset_tokens OWNER TO mailforge_user;

--
-- Name: password_reset_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: mailforge_user
--

CREATE SEQUENCE public.password_reset_tokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.password_reset_tokens_id_seq OWNER TO mailforge_user;

--
-- Name: password_reset_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mailforge_user
--

ALTER SEQUENCE public.password_reset_tokens_id_seq OWNED BY public.password_reset_tokens.id;


--
-- Name: placement_results; Type: TABLE; Schema: public; Owner: mailforge_user
--

CREATE TABLE public.placement_results (
    id integer NOT NULL,
    campaign_id integer,
    provider character varying(100),
    folder character varying(100),
    message_id character varying(255),
    checked_at timestamp without time zone
);


ALTER TABLE public.placement_results OWNER TO mailforge_user;

--
-- Name: placement_results_id_seq; Type: SEQUENCE; Schema: public; Owner: mailforge_user
--

CREATE SEQUENCE public.placement_results_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.placement_results_id_seq OWNER TO mailforge_user;

--
-- Name: placement_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mailforge_user
--

ALTER SEQUENCE public.placement_results_id_seq OWNED BY public.placement_results.id;


--
-- Name: recipients; Type: TABLE; Schema: public; Owner: mailforge_user
--

CREATE TABLE public.recipients (
    id integer NOT NULL,
    tenant_id integer,
    email character varying(320) NOT NULL,
    name character varying(255),
    metadata json DEFAULT '{}'::jsonb,
    is_valid boolean DEFAULT true,
    validation_reason character varying(255),
    contact_status character varying(50) DEFAULT 'valid'::character varying NOT NULL,
    message_status character varying(50) DEFAULT 'queued'::character varying NOT NULL,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.recipients OWNER TO mailforge_user;

--
-- Name: recipients_id_seq; Type: SEQUENCE; Schema: public; Owner: mailforge_user
--

CREATE SEQUENCE public.recipients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.recipients_id_seq OWNER TO mailforge_user;

--
-- Name: recipients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mailforge_user
--

ALTER SEQUENCE public.recipients_id_seq OWNED BY public.recipients.id;


--
-- Name: refresh_tokens; Type: TABLE; Schema: public; Owner: mailforge_user
--

CREATE TABLE public.refresh_tokens (
    id integer NOT NULL,
    user_id integer NOT NULL,
    token_hash character varying(255) NOT NULL,
    expires_at timestamp without time zone NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.refresh_tokens OWNER TO mailforge_user;

--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: mailforge_user
--

CREATE SEQUENCE public.refresh_tokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.refresh_tokens_id_seq OWNER TO mailforge_user;

--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mailforge_user
--

ALTER SEQUENCE public.refresh_tokens_id_seq OWNED BY public.refresh_tokens.id;


--
-- Name: seed_inboxes; Type: TABLE; Schema: public; Owner: mailforge_user
--

CREATE TABLE public.seed_inboxes (
    id integer NOT NULL,
    tenant_id integer,
    provider character varying(50),
    email character varying(320) NOT NULL,
    imap_host character varying(255),
    imap_port integer,
    imap_user character varying(255),
    encrypted_imap_password text,
    spam_folder character varying(100),
    inbox_folder character varying(100),
    created_at timestamp without time zone
);


ALTER TABLE public.seed_inboxes OWNER TO mailforge_user;

--
-- Name: seed_inboxes_id_seq; Type: SEQUENCE; Schema: public; Owner: mailforge_user
--

CREATE SEQUENCE public.seed_inboxes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seed_inboxes_id_seq OWNER TO mailforge_user;

--
-- Name: seed_inboxes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mailforge_user
--

ALTER SEQUENCE public.seed_inboxes_id_seq OWNED BY public.seed_inboxes.id;


--
-- Name: smtp_accounts; Type: TABLE; Schema: public; Owner: mailforge_user
--

CREATE TABLE public.smtp_accounts (
    id integer NOT NULL,
    tenant_id integer,
    name character varying(255),
    host character varying(255) NOT NULL,
    port integer,
    username character varying(255),
    encrypted_password text,
    is_active boolean,
    last_failure_at timestamp without time zone,
    fail_count integer DEFAULT 0 NOT NULL,
    last_used_at timestamp without time zone,
    rate_limit integer,
    created_at timestamp without time zone,
    security character varying(10)
);


ALTER TABLE public.smtp_accounts OWNER TO mailforge_user;

--
-- Name: smtp_accounts_id_seq; Type: SEQUENCE; Schema: public; Owner: mailforge_user
--

CREATE SEQUENCE public.smtp_accounts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.smtp_accounts_id_seq OWNER TO mailforge_user;

--
-- Name: smtp_accounts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mailforge_user
--

ALTER SEQUENCE public.smtp_accounts_id_seq OWNED BY public.smtp_accounts.id;


--
-- Name: suppressions; Type: TABLE; Schema: public; Owner: mailforge_user
--

CREATE TABLE public.suppressions (
    id integer NOT NULL,
    tenant_id integer,
    email character varying(320),
    reason character varying(255),
    created_at timestamp without time zone
);


ALTER TABLE public.suppressions OWNER TO mailforge_user;

--
-- Name: suppressions_id_seq; Type: SEQUENCE; Schema: public; Owner: mailforge_user
--

CREATE SEQUENCE public.suppressions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.suppressions_id_seq OWNER TO mailforge_user;

--
-- Name: suppressions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mailforge_user
--

ALTER SEQUENCE public.suppressions_id_seq OWNED BY public.suppressions.id;


--
-- Name: tenant_messages; Type: TABLE; Schema: public; Owner: mailforge_user
--

CREATE TABLE public.tenant_messages (
    id integer NOT NULL,
    tenant_id integer NOT NULL,
    message character varying(1024) NOT NULL,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.tenant_messages OWNER TO mailforge_user;

--
-- Name: tenant_messages_id_seq; Type: SEQUENCE; Schema: public; Owner: mailforge_user
--

CREATE SEQUENCE public.tenant_messages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tenant_messages_id_seq OWNER TO mailforge_user;

--
-- Name: tenant_messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mailforge_user
--

ALTER SEQUENCE public.tenant_messages_id_seq OWNED BY public.tenant_messages.id;


--
-- Name: tenants; Type: TABLE; Schema: public; Owner: mailforge_user
--

CREATE TABLE public.tenants (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    created_at timestamp without time zone,
    company_name character varying(255),
    industry character varying(255),
    team_size integer
);


ALTER TABLE public.tenants OWNER TO mailforge_user;

--
-- Name: tenants_id_seq; Type: SEQUENCE; Schema: public; Owner: mailforge_user
--

CREATE SEQUENCE public.tenants_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tenants_id_seq OWNER TO mailforge_user;

--
-- Name: tenants_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mailforge_user
--

ALTER SEQUENCE public.tenants_id_seq OWNED BY public.tenants.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: mailforge_user
--

CREATE TABLE public.users (
    id integer NOT NULL,
    tenant_id integer,
    email character varying(255) NOT NULL,
    hashed_password character varying(255) NOT NULL,
    role public.roleenum,
    created_at timestamp without time zone
);


ALTER TABLE public.users OWNER TO mailforge_user;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: mailforge_user
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO mailforge_user;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mailforge_user
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: blacklisted_tokens id; Type: DEFAULT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.blacklisted_tokens ALTER COLUMN id SET DEFAULT nextval('public.blacklisted_tokens_id_seq'::regclass);


--
-- Name: campaign_batches id; Type: DEFAULT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.campaign_batches ALTER COLUMN id SET DEFAULT nextval('public.campaign_batches_id_seq'::regclass);


--
-- Name: campaigns id; Type: DEFAULT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.campaigns ALTER COLUMN id SET DEFAULT nextval('public.campaigns_id_seq'::regclass);


--
-- Name: message_logs id; Type: DEFAULT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.message_logs ALTER COLUMN id SET DEFAULT nextval('public.message_logs_id_seq'::regclass);


--
-- Name: password_reset_tokens id; Type: DEFAULT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.password_reset_tokens ALTER COLUMN id SET DEFAULT nextval('public.password_reset_tokens_id_seq'::regclass);


--
-- Name: placement_results id; Type: DEFAULT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.placement_results ALTER COLUMN id SET DEFAULT nextval('public.placement_results_id_seq'::regclass);


--
-- Name: recipients id; Type: DEFAULT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.recipients ALTER COLUMN id SET DEFAULT nextval('public.recipients_id_seq'::regclass);


--
-- Name: refresh_tokens id; Type: DEFAULT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.refresh_tokens ALTER COLUMN id SET DEFAULT nextval('public.refresh_tokens_id_seq'::regclass);


--
-- Name: seed_inboxes id; Type: DEFAULT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.seed_inboxes ALTER COLUMN id SET DEFAULT nextval('public.seed_inboxes_id_seq'::regclass);


--
-- Name: smtp_accounts id; Type: DEFAULT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.smtp_accounts ALTER COLUMN id SET DEFAULT nextval('public.smtp_accounts_id_seq'::regclass);


--
-- Name: suppressions id; Type: DEFAULT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.suppressions ALTER COLUMN id SET DEFAULT nextval('public.suppressions_id_seq'::regclass);


--
-- Name: tenant_messages id; Type: DEFAULT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.tenant_messages ALTER COLUMN id SET DEFAULT nextval('public.tenant_messages_id_seq'::regclass);


--
-- Name: tenants id; Type: DEFAULT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.tenants ALTER COLUMN id SET DEFAULT nextval('public.tenants_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: mailforge_user
--

COPY public.alembic_version (version_num) FROM stdin;
54abd4796b7d
\.


--
-- Data for Name: blacklisted_tokens; Type: TABLE DATA; Schema: public; Owner: mailforge_user
--

COPY public.blacklisted_tokens (id, token, expires_at, created_at) FROM stdin;
\.


--
-- Data for Name: campaign_batches; Type: TABLE DATA; Schema: public; Owner: mailforge_user
--

COPY public.campaign_batches (id, campaign_id, status, sent_at, meta, batch_index) FROM stdin;
1	1	failed	2025-10-03 16:54:45.102494	{}	1
2	20	failed	2025-10-04 20:42:26.918077	{"size": 1}	0
\.


--
-- Data for Name: campaigns; Type: TABLE DATA; Schema: public; Owner: mailforge_user
--

COPY public.campaigns (id, tenant_id, name, subject, body, sender, status, ai_score, ai_suggestions, created_at, query, local_kw, recheck_every_batches, recheck_every_minutes, max_consecutive_spam, show_badge) FROM stdin;
16	7	gg	fggg	<p>Hello [First Name],</p>\n                                <p><br></p>\n                                <p>We're excited to share our latest updates with you...</p>\n                                <p><br></p>\n                                <p>Best regards,<br>The Team</p>	herr <fa5705980a1d7c>	draft	9.5	["Subject might be too short"]	2025-10-03 19:14:36.455329	{}	{}	5	10	2	f
3	7	ffff	gggg	<p>Hello [First Name],</p>\n                                <p><br></p>\n                                <p>We're excited to share our latest updates with you...</p>\n                                <p><br></p>\n                                <p>Best regards,<br>The Team</p>	newsletter@yourdomain.com	paused	9.5	["Subject might be too short"]	2025-10-02 20:13:03.863962	{}	{}	5	10	2	t
1	\N	Test Campaign	Hello	<p>Hi there</p>	support@yourdomain.com	failed	\N	\N	2025-10-02 07:54:52.443407	{}	{"keyword": "value"}	5	10	2	f
17	7	gg	fggg	<p>Hello [First Name],</p>\n                                <p><br></p>\n                                <p>We're excited to share our latest updates with you...</p>\n                                <p><br></p>\n                                <p>Best regards,<br>The Team</p>	herr <fa5705980a1d7c>	draft	9.5	["Subject might be too short"]	2025-10-03 19:30:12.561852	{}	{}	5	10	2	f
4	7	hey	fggg	<p>Hello [First Name],</p>\n                                <p><br></p>\n                                <p>We're excited to share our latest updates with you...</p>\n                                <p><br></p>\n                                <p>Best regards,<br>The Team</p>	hry boi <fa5705980a1d7c>	draft	9.5	["Subject might be too short"]	2025-10-03 12:36:59.467527	{}	{}	5	10	2	f
5	7	gg	ggg	<p>Hello [First Name],</p>\n                                <p><br></p>\n                                <p>We're excited to share our latest updates with you...</p>\n                                <p><br></p>\n                                <p>Best regards,<br>The Team</p>	hi man <fa5705980a1d7c>	draft	9.5	["Subject might be too short"]	2025-10-03 13:50:33.512277	{}	{}	5	10	2	f
6	7	gg	fggg	<p>Hello [First Name],</p>\n                                <p><br></p>\n                                <p>We're excited to share our latest updates with you...</p>\n                                <p><br></p>\n                                <p>Best regards,<br>The Teamfff</p>	fff <fa5705980a1d7c>	draft	9.5	["Subject might be too short"]	2025-10-03 14:56:27.54027	{}	{}	5	10	2	f
7	7	gg	fggg	<p>Hello [First Name],</p>\n                                <p><br></p>\n                                <p>We're excited to share our latest updates with you...</p>\n                                <p><br></p>\n                                <p>Best regards,<br>The Team</p>	ffff <fa5705980a1d7c>	draft	9.5	["Subject might be too short"]	2025-10-03 15:50:01.02305	{}	{}	5	10	2	f
8	7	gg	fggg	<p>Hello [First Name],</p>\n                                <p><br></p>\n                                <p>We're excited to share our latest updates with you...</p>\n                                <p><br></p>\n                                <p>Best regards,<br>The Team</p>	yuuu <fa5705980a1d7c>	draft	9.5	["Subject might be too short"]	2025-10-03 16:13:19.447375	{}	{}	5	10	2	f
9	7	gg	fggg	<p>Hello [First Name],</p>\n                                <p><br></p>\n                                <p>We're excited to share our latest updates with you...</p>\n                                <p><br></p>\n                                <p>Best regards,<br>The Team</p>	fgg <fa5705980a1d7c>	draft	9.5	["Subject might be too short"]	2025-10-03 16:20:45.385997	{}	{}	5	10	2	f
2	7	Welcome Campaign	Welcome to MailForge 🚀	<p>Hello there!<br>Thanks for joining us.</p>	fa5705980a1d7c@fa5705980a1d7c	failed	8.5	["Consider removing emoji for better deliverability"]	2025-10-02 19:40:53.495841	{}	{}	5	10	2	f
10	7	gg	fggg	<p>Hello [First Name],</p>\n                                <p><br></p>\n                                <p>We're excited to share our latest updates with you...</p>\n                                <p><br></p>\n                                <p>Best regards,<br>The Team</p>	herr <fa5705980a1d7c>	draft	9.5	["Subject might be too short"]	2025-10-03 17:20:03.527798	{}	{}	5	10	2	f
11	7	gg	fggg	<p>Hello [First Name],</p>\n                                <p><br></p>\n                                <p>We're cccexcited to share our latest updates with you...</p>\n                                <p><br></p>\n                                <p>Best regards,<br>The Team</p>	herr <fa5705980a1d7c>	draft	9.5	["Subject might be too short"]	2025-10-03 17:53:08.42915	{}	{}	5	10	2	f
12	7	gg	fggg	<p>Hello [First Name],</p>\n                                <p><br></p>\n                                <p>We'rejk excited to share our latest updates with you...</p>\n                                <p><br></p>\n                                <p>Best regards,<br>The Team</p>	herr <fa5705980a1d7c>	draft	9.5	["Subject might be too short"]	2025-10-03 18:05:50.566821	{}	{}	5	10	2	f
13	7	gg	fggg	<p>Hello [First Name],</p>\n                                <p><br></p>\n                                <p>We're excited to share our latest updates with you...</p>\n                                <p><br></p>\n                                <p>Best regards,<br>The Team</p>	herr <fa5705980a1d7c>	draft	9.5	["Subject might be too short"]	2025-10-03 18:19:38.02891	{}	{}	5	10	2	f
14	7	gg	fggg	<p>Hello [First Name],</p>\n                                <p><br></p>\n                                <p>We're excited to share our latest updates with you...</p>\n                                <p><br></p>\n                                <p>Best regards,<br>The Team</p>	herr <fa5705980a1d7c>	draft	9.5	["Subject might be too short"]	2025-10-03 18:22:55.587945	{}	{}	5	10	2	f
15	7	gg	fggg	<p>Hello [First Name],</p>\n                                <p><br></p>\n                                <p>We're excited to share our latest updates with you...</p>\n                                <p><br></p>\n                                <p>Best regards,<br>The Team</p>	herr <fa5705980a1d7c>	draft	9.5	["Subject might be too short"]	2025-10-03 18:44:52.620414	{}	{}	5	10	2	f
18	7	gg	fggg	<p>Hello [First Name],</p>\n                                <p><br></p>\n                                <p>We're excited to share our latest updates with you...</p>\n                                <p><br></p>\n                                <p>Best regards,<br>The Team</p>	herr <fa5705980a1d7c>	draft	9.5	["Subject might be too short"]	2025-10-03 19:31:32.414045	{}	{}	5	10	2	f
19	7	gg	fggg	<p>Hello [First Name],</p>\n                                <p><br></p>\n                                <p>We're excited to share our latest updates with you...</p>\n                                <p><br></p>\n                                <p>Best regards,<br>The Team</p>	herr <fa5705980a1d7c>	draft	9.5	["Subject might be too short"]	2025-10-04 20:28:44.341147	{}	{}	5	10	2	f
20	7	gg	fggg	<p>Hello [First Name],</p>\n                                <p><br></p>\n                                <p>We're excited to share our latest updates with you...</p>\n                                <p><br></p>\n                                <p>Best regards,<br>The Team</p>	herr <fa5705980a1d7c>	failed	9.5	["Subject might be too short"]	2025-10-04 20:42:22.580699	{}	{}	5	10	2	f
\.


--
-- Data for Name: message_logs; Type: TABLE DATA; Schema: public; Owner: mailforge_user
--

COPY public.message_logs (id, tenant_id, campaign_id, recipient, smtp_id, status, details, created_at) FROM stdin;
1	7	\N	nfgdf@mail.com	11	sent	{"subject": "Hello"}	2025-10-03 11:15:49.479961
\.


--
-- Data for Name: password_reset_tokens; Type: TABLE DATA; Schema: public; Owner: mailforge_user
--

COPY public.password_reset_tokens (id, user_id, token_hash, expires_at, used, created_at) FROM stdin;
\.


--
-- Data for Name: placement_results; Type: TABLE DATA; Schema: public; Owner: mailforge_user
--

COPY public.placement_results (id, campaign_id, provider, folder, message_id, checked_at) FROM stdin;
\.


--
-- Data for Name: recipients; Type: TABLE DATA; Schema: public; Owner: mailforge_user
--

COPY public.recipients (id, tenant_id, email, name, metadata, is_valid, validation_reason, contact_status, message_status, created_at) FROM stdin;
1	7	lakoto9754@bitmens.com	Lakoto Test	{}	t	\N	valid	queued	2025-10-03 20:21:29.333078
547	1	test@example.com	Test User	{}	t	\N	valid	queued	2025-10-04 16:33:03.865183
548	1	test@example.com	Test User	{}	t		valid	queued	2025-10-04 16:34:58.253944
549	1	dhsh@kdsk.com	\N	{}	t		valid	queued	2025-10-04 16:34:58.272586
550	1	snmv*kf@mail.com	\N	{}	t		valid	queued	2025-10-04 16:34:58.275375
551	1	palimenstadl@web.de	\N	{}	t		valid	queued	2025-10-04 16:34:58.27603
552	1	kmtrialsport@web.de	\N	{}	t		valid	queued	2025-10-04 16:34:58.277297
553	1	vdsibremen@web.de	\N	{}	t		valid	queued	2025-10-04 16:34:58.27855
554	1	peter-heim-gmbh@web.de	\N	{}	t		valid	queued	2025-10-04 16:34:58.279889
555	1	uebersetzungen-mayer@web.de	\N	{}	t		valid	queued	2025-10-04 16:34:58.281127
556	1	j.a.r.t.stallbaugmbh@web.de	\N	{}	t		valid	queued	2025-10-04 16:34:58.282821
557	1	udo.willerscheid@web.de	\N	{}	t		valid	queued	2025-10-04 16:34:58.283231
558	1	sonnenquell@web.de	\N	{}	t		valid	queued	2025-10-04 16:34:58.283674
559	1	schlosserei-a.mueller@web.de	\N	{}	t		valid	queued	2025-10-04 16:34:58.284112
560	1	mineraloele-albert@web.de	\N	{}	t		valid	queued	2025-10-04 16:34:58.284639
561	1	jacob-atemschutz@web.de	\N	{}	t		valid	queued	2025-10-04 16:34:58.28567
562	1	schaeferei-berger@web.de	\N	{}	t		valid	queued	2025-10-04 16:34:58.286096
563	1	hydro-logo@web.de	\N	{}	t		valid	queued	2025-10-04 16:34:58.286496
564	1	andreas.v.heymann@web.de	\N	{}	t		valid	queued	2025-10-04 16:34:58.286861
565	1	steffen_henze@web.de	\N	{}	t		valid	queued	2025-10-04 16:34:58.287243
566	1	fliesen-wespel@web.de	\N	{}	t		valid	queued	2025-10-04 16:34:58.287719
567	1	georg.hartfuss@web.de	\N	{}	t		valid	queued	2025-10-04 16:34:58.288124
568	1	jr-textil-design@web.de	\N	{}	t		valid	queued	2025-10-04 16:34:58.288558
569	1	ebacom@web.de	\N	{}	t		valid	queued	2025-10-04 16:34:58.288967
570	1	pro_agrar@web.de	\N	{}	t		valid	queued	2025-10-04 16:34:58.289397
571	1	d-ganske@web.de	\N	{}	t		valid	queued	2025-10-04 16:34:58.289787
572	1	hghnhf@mail.com	\N	{}	t		valid	queued	2025-10-04 16:34:58.290206
573	1	ddd@mail.com	\N	{}	t		valid	queued	2025-10-04 16:34:58.290599
574	1	Dhfhsdb@mail.com	\N	{}	t		valid	queued	2025-10-04 16:34:58.290958
\.


--
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: public; Owner: mailforge_user
--

COPY public.refresh_tokens (id, user_id, token_hash, expires_at, created_at) FROM stdin;
2	3	$2b$12$ErNNMtcSYW4gs2jEgLhwB.1SenloOV4MU6/zyW2SXGqZUbcXGP3wK	2025-10-02 18:25:02.437112	2025-09-25 18:25:02.438945
3	4	$2b$12$izFPnkl12wYeDVqbTfA8SudeOapymbco5Hib2XAMxWt7if2oL1lmS	2025-10-02 20:42:50.12789	2025-09-25 20:42:50.13201
4	5	$2b$12$Hbw0I/2ktM4YvnoNmXATEO9l8z2gL.oKwF5yvkxLXiUHUvivvKu.6	2025-10-02 21:50:58.480087	2025-09-25 21:50:58.481016
5	6	$2b$12$1EdqfN1vxOSf0sZyVlW5/.k/K7pXzqujP2xjdhPBFJga81pP8Y0eO	2025-10-02 23:16:58.998362	2025-09-25 23:16:59.001984
70	7	$2b$12$KhvIZ0SxoxgNtQBn1DMeLOgPyj6G4ft8DfuunKG8E2N2A0ZSFp3mi	2025-10-11 03:25:30.741188	2025-10-04 03:25:30.743552
71	7	$2b$12$eGa8mNq78oxk60pRQnlLO.neqLwCBvWk6Q8pbOrNbUynlq31nFB/W	2025-10-11 18:06:47.285625	2025-10-04 18:06:47.287443
72	8	$2b$12$f27Y/14u3kyAZEu6hUS1OeAgHBekMELFBPF6rLFVsA6bv1UxdITd2	2025-10-12 21:09:36.67194	2025-10-05 21:09:36.673474
73	9	$2b$12$QDZaNDljYD1HY1yEMRec6.WoG3bP9Ug5zBZKiOjq/.EMAdnJiN8X2	2025-10-12 21:40:36.937149	2025-10-05 21:40:36.938341
74	10	$2b$12$b4g39FVLFCS4hukqM/WKVO3EmVt6dqytH8kJI5c53F1oV2xS6.KAe	2025-10-12 21:46:57.233916	2025-10-05 21:46:57.235314
75	11	$2b$12$Mat8YZJx/XOlHiU3RCkk.eXWaPKZx5dDC18ox7TPC4.3Q.ayhVT/W	2025-10-12 21:49:28.133054	2025-10-05 21:49:28.134522
76	12	$2b$12$ofWswXA04vHYs0.U2jasSeK7fOqzNAO7ByxN06i7c1NJahVqZA7o2	2025-10-12 21:49:39.217895	2025-10-05 21:49:39.218432
77	13	$2b$12$n1R/z87bxtRunvwVkV2WguFUTYsD7jtmcmhJHcxl32tCBhXV5lPbK	2025-10-12 21:50:04.032428	2025-10-05 21:50:04.032934
78	14	$2b$12$oL3UqAcvpaCa9oAopfULG.TP/Win2/5.tfeOTrjh5xZzJQxtYInE6	2025-10-12 22:32:56.181858	2025-10-05 22:32:56.183262
79	15	$2b$12$99fPkhphzeLyZWoyekVwZOLTBpLVe6QvmvLaVE2AmzslCDi6tdIje	2025-10-12 22:40:37.878145	2025-10-05 22:40:37.878697
82	17	$2b$12$Ut6QJ8Kej3meEn4ST3Jn0e2511nZX3RbXAB62ZzEG4tQMtf.h69UW	2025-10-12 23:01:31.38637	2025-10-05 23:01:31.387549
\.


--
-- Data for Name: seed_inboxes; Type: TABLE DATA; Schema: public; Owner: mailforge_user
--

COPY public.seed_inboxes (id, tenant_id, provider, email, imap_host, imap_port, imap_user, encrypted_imap_password, spam_folder, inbox_folder, created_at) FROM stdin;
\.


--
-- Data for Name: smtp_accounts; Type: TABLE DATA; Schema: public; Owner: mailforge_user
--

COPY public.smtp_accounts (id, tenant_id, name, host, port, username, encrypted_password, is_active, last_failure_at, fail_count, last_used_at, rate_limit, created_at, security) FROM stdin;
11	7	Mailtrap Sandbox	sandbox.smtp.mailtrap.io	2525	fa5705980a1d7c	gAAAAABo3tOoDHj4Y_YvApQvK_SClByqWPa5TCji3JgF6m4ZrdT6dFmBBAAmB71nbOASupIN7YbDpBuh-irB_835zr3y4MuaPA==	f	2025-10-03 11:46:05.288579	5	2025-10-03 11:15:49.477444	100	2025-10-02 19:34:00.918243	tls
8	7	sandbox.smtp.mailtrap.io	sandbox.smtp.mailtrap.io	2525	d0dbacc4119a3d	gAAAAABo2FCtC1ZZR9xUXPmdayvPXkuBTxafHQSuDStRJJtEWKPjAczIp-odp1uc8QGPNB2fRByoViM_AC3fH4Hxy1SREij3Sw==	f	2025-09-28 02:57:28.486561	5	\N	1000	2025-09-27 21:01:33.641709	tls
10	7	support@bitmens.com	smtp.mailtrap.io	587	username	password	\N	\N	0	\N	\N	\N	\N
12	1	Mailtrap Sandbox	sandbox.smtp.mailtrap.io	2525	b0bd0b50b1869d	bb85e465190d4e	f	2025-10-03 11:29:19.199658	5	\N	\N	\N	tls
\.


--
-- Data for Name: suppressions; Type: TABLE DATA; Schema: public; Owner: mailforge_user
--

COPY public.suppressions (id, tenant_id, email, reason, created_at) FROM stdin;
\.


--
-- Data for Name: tenant_messages; Type: TABLE DATA; Schema: public; Owner: mailforge_user
--

COPY public.tenant_messages (id, tenant_id, message, created_at) FROM stdin;
1	7	⚠️ SMTP 168c3aa181c323@sandbox.smtp.mailtrap.io failed: ❌ SMTPServerDisconnected: Unexpected EOF received	2025-09-27 01:48:46.684584
2	7	⚠️ SMTP 168c3aa181c323@sandbox.smtp.mailtrap.io failed: ❌ SMTPServerDisconnected: Unexpected EOF received	2025-09-27 01:49:31.030092
3	7	🚨 Deactivated 168c3aa181c323@sandbox.smtp.mailtrap.io after 5 failures.	2025-09-27 01:49:31.035551
4	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 20:35:55.324319
5	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 20:42:27.369213
6	7	✅ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io recovered and is active again.	2025-09-27 20:47:53.30556
7	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPConnectError: Error connecting to sandbox.smtp.mailtrap.io on port 2525: 	2025-09-27 20:47:58.342456
8	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 20:52:18.282228
9	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 20:52:22.382579
10	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 21:07:31.755098
11	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 21:07:36.665915
12	7	✅ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io recovered and is active again.	2025-09-27 21:07:42.886118
13	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 21:22:50.421197
14	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 21:22:54.322457
15	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 21:38:06.975434
16	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 21:38:10.5537
17	7	✅ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io recovered and is active again.	2025-09-27 21:38:14.268925
18	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 21:53:21.887753
19	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 21:53:26.760354
20	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 21:55:39.014229
21	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 21:55:42.24869
22	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 21:55:45.421857
23	7	🚨 Deactivated d0dbacc4119a3d@sandbox.smtp.mailtrap.io after 5 failures.	2025-09-27 21:55:45.42459
24	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 22:03:55.439547
25	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 22:03:58.757588
26	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 22:04:01.773171
27	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 22:04:25.220974
28	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 22:04:28.256242
29	7	🚨 Deactivated d0dbacc4119a3d@sandbox.smtp.mailtrap.io after 5 failures.	2025-09-27 22:04:28.258134
30	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 22:04:31.413535
31	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 22:05:26.626193
32	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 22:05:29.986268
33	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 22:10:47.626072
34	7	🚨 Deactivated d0dbacc4119a3d@sandbox.smtp.mailtrap.io after 5 failures.	2025-09-27 22:10:47.631244
35	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 22:10:51.387777
36	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-09-27 22:17:03.769927
37	7	🚨 Deactivated d0dbacc4119a3d@sandbox.smtp.mailtrap.io after 5 failures.	2025-09-27 22:17:03.784661
38	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPReadTimeoutError: Timed out waiting for server response	2025-09-27 22:33:23.679858
39	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPConnectError: Error connecting to sandbox.smtp.mailtrap.io on port 2525: [Errno 8] nodename nor servname provided, or not known	2025-09-27 22:48:23.769208
40	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPConnectError: Error connecting to sandbox.smtp.mailtrap.io on port 2525: [Errno 8] nodename nor servname provided, or not known	2025-09-27 23:03:23.860613
41	7	✅ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io recovered and is active again.	2025-09-28 00:35:34.869479
42	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPReadTimeoutError: Timed out waiting for server response	2025-09-28 01:19:26.733831
43	7	✅ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io recovered and is active again.	2025-09-28 01:29:50.87624
44	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPServerDisconnected: Unexpected EOF received	2025-09-28 02:35:17.455053
45	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPServerDisconnected: Unexpected EOF received	2025-09-28 02:41:47.950172
46	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPServerDisconnected: Unexpected EOF received	2025-09-28 02:43:33.978824
47	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPServerDisconnected: Unexpected EOF received	2025-09-28 02:44:06.407691
48	7	⚠️ SMTP d0dbacc4119a3d@sandbox.smtp.mailtrap.io failed: ❌ SMTPServerDisconnected: Unexpected EOF received	2025-09-28 02:57:28.499593
49	7	🚨 Deactivated d0dbacc4119a3d@sandbox.smtp.mailtrap.io after 5 failures.	2025-09-28 02:57:28.509878
50	7	⚠️ SMTP fa5705980a1d7c@sandbox.smtp.mailtrap.io failed: ❌ SMTPTimeoutError: SSL handshake is taking longer than 5 seconds: aborting the connection	2025-10-02 20:06:19.653734
51	7	✅ SMTP fa5705980a1d7c@sandbox.smtp.mailtrap.io recovered and is active again.	2025-10-02 20:12:50.374271
52	7	⚠️ SMTP fa5705980a1d7c@sandbox.smtp.mailtrap.io failed: ❌ SMTPConnectError: Error connecting to sandbox.smtp.mailtrap.io on port 2525: 	2025-10-02 21:13:11.515156
53	7	✅ SMTP fa5705980a1d7c@sandbox.smtp.mailtrap.io recovered and is active again.	2025-10-02 21:28:14.992409
54	7	⚠️ SMTP fa5705980a1d7c@sandbox.smtp.mailtrap.io failed: ❌ SMTPDataError: (550, '5.7.0 Too many emails per second. Please upgrade your plan https://mailtrap.io/billing/plans/testing')	2025-10-03 10:37:00.47856
55	7	✅ SMTP fa5705980a1d7c@sandbox.smtp.mailtrap.io recovered and is active again.	2025-10-03 11:23:03.33132
56	1	⚠️ SMTP b0bd0b50b1869d@sandbox.smtp.mailtrap.io failed: ❌ InvalidToken: 	2025-10-03 11:23:03.348821
57	1	⚠️ SMTP b0bd0b50b1869d@sandbox.smtp.mailtrap.io failed: ❌ InvalidToken: 	2025-10-03 11:23:53.030542
58	1	⚠️ SMTP b0bd0b50b1869d@sandbox.smtp.mailtrap.io failed: ❌ InvalidToken: 	2025-10-03 11:26:41.305232
59	1	⚠️ SMTP b0bd0b50b1869d@sandbox.smtp.mailtrap.io failed: ❌ InvalidToken: 	2025-10-03 11:27:48.022382
60	7	⚠️ SMTP fa5705980a1d7c@sandbox.smtp.mailtrap.io failed: ❌ SMTPServerDisconnected: Unexpected EOF received	2025-10-03 11:29:19.190587
61	1	⚠️ SMTP b0bd0b50b1869d@sandbox.smtp.mailtrap.io failed: ❌ InvalidToken: 	2025-10-03 11:29:19.200038
62	1	🚨 Deactivated b0bd0b50b1869d@sandbox.smtp.mailtrap.io after 5 failures.	2025-10-03 11:29:19.201296
63	7	⚠️ SMTP fa5705980a1d7c@sandbox.smtp.mailtrap.io failed: ❌ SMTPServerDisconnected: Unexpected EOF received	2025-10-03 11:38:37.713466
64	7	⚠️ SMTP fa5705980a1d7c@sandbox.smtp.mailtrap.io failed: ❌ SMTPServerDisconnected: Unexpected EOF received	2025-10-03 11:39:38.069129
65	7	⚠️ SMTP fa5705980a1d7c@sandbox.smtp.mailtrap.io failed: ❌ SMTPServerDisconnected: Unexpected EOF received	2025-10-03 11:42:28.378629
66	7	⚠️ SMTP fa5705980a1d7c@sandbox.smtp.mailtrap.io failed: ❌ SMTPServerDisconnected: Unexpected EOF received	2025-10-03 11:46:05.301626
67	7	🚨 Deactivated fa5705980a1d7c@sandbox.smtp.mailtrap.io after 5 failures.	2025-10-03 11:46:05.31205
\.


--
-- Data for Name: tenants; Type: TABLE DATA; Schema: public; Owner: mailforge_user
--

COPY public.tenants (id, name, created_at, company_name, industry, team_size) FROM stdin;
1	TestTenant	\N	Test Company	Software	10
2	jhay	2025-09-25 18:13:13.963461	\N	\N	\N
3	jay	2025-09-25 18:25:01.811494	\N	\N	\N
4	hey	2025-09-25 20:42:49.566378	\N	\N	\N
5	lov	2025-09-25 21:50:57.931276	\N	\N	\N
6	james	2025-09-25 23:16:58.391586	\N	\N	\N
9	TestTenantX	2025-10-05 21:09:35.802089	\N	\N	\N
10	DevTenant	2025-10-05 21:40:36.275081	\N	\N	\N
13	DevTenant-1759700816	2025-10-05 21:46:56.460941	\N	\N	\N
14	DevTenant-1759700967	2025-10-05 21:49:27.243964	\N	\N	\N
15	DevTenant-1759700978	2025-10-05 21:49:38.413175	\N	\N	\N
16	SomeDuplicateTenant-TEST	2025-10-05 21:50:03.247015	\N	\N	\N
18	DevTenant-1759703575	2025-10-05 22:32:55.265499	\N	\N	\N
19	DevTenant-1759704037	2025-10-05 22:40:37.063	\N	\N	\N
20	DevTenant-1759704094	2025-10-05 22:41:34.428304	\N	\N	\N
21	DevTenant-1759705285	2025-10-05 23:01:25.80854	\N	\N	\N
7	jen	2025-09-26 01:22:38.343489	TestCo	Software	10
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: mailforge_user
--

COPY public.users (id, tenant_id, email, hashed_password, role, created_at) FROM stdin;
1	1	admin@example.com	hashed_password_here	owner	\N
2	2	brianpinksen11@gmail.com	$2b$12$HydEJ5FP6Cx58fg4gMj0kOppa0rSrrU.oxIhlpiqvhX2bCpF6kyea	owner	2025-09-25 18:13:14.262353
3	3	363ty@mail.com	$2b$12$CF/x79oY8THhWZu5S6o4p.4Fc85luMBkfG5rVDzUzJcCS1t9Zg5Bm	owner	2025-09-25 18:25:02.090609
4	4	yilepiw268@bitmens.com	$2b$12$PRTvs9URSTxQqmyrG4lSBOCIQqC95Lpcc32QCN2OLNRS3Q9Y.rmp6	owner	2025-09-25 20:42:49.854325
5	5	xojeg78661@auslank.com	$2b$12$3Y6nI4Y8V5UHT7lUCq.fseDW0bArkv54RcEqW.gUjSV9wjzGoF34K	owner	2025-09-25 21:50:58.202859
6	6	womanib183@auslank.com	$2b$12$5MCXzeCHUQQcCtv2QyXPZuF/FdoGklItw1mD7VSMdCBfctUZ9wvzC	owner	2025-09-25 23:16:58.709324
7	7	lakoto9754@bitmens.com	$2b$12$EpGSneOyKPqlJeBdfUKsKen/vYU5/gE9Ei3lF/SQJ.GVDgXj.hepe	owner	2025-09-26 01:22:38.695295
8	9	test+signupX@example.com	$2b$12$rH6RB12p8VyiQGGhJ2dPJex1scn8FtOVgxJhJZ/sjdkVLFwa/1Qem	owner	2025-10-05 21:09:36.242045
9	10	dev+signup@example.com	$2b$12$7jDmdX.ecfDDWjFhBS2/UORteiSz4Qt9u7JvAH4I/K3jDoOAiDkd2	owner	2025-10-05 21:40:36.620773
10	13	dev+1759700816@example.com	$2b$12$Fj7DadNyCoJs54AuspZM..hgHMz1OCsnPml/bQCZOd/xsgxb.E83G	owner	2025-10-05 21:46:56.863546
11	14	dev+1759700967@example.com	$2b$12$9AE7MRX56kcx/76H/Hz78O9WmxXov8rqRQqU2vbxr8tP5PWuqsSt2	owner	2025-10-05 21:49:27.708205
12	15	dev+1759700978@example.com	$2b$12$Y3AQ5VvH.pGaZ7HF4CyerulY98X.PpkaQwMBUcoxly6O7GN71FJzW	owner	2025-10-05 21:49:38.814364
13	16	dup1+1759701003@example.com	$2b$12$dKSmLSonKQsmwhvnpu.x9eG542b3x16Vo2wsTE083lD6Hw.8.LQ.W	owner	2025-10-05 21:50:03.641501
14	18	dev+1759703575@example.com	$2b$12$aQF/Z110VKEUjUQqFizjR.orkWurwoacTJaA.KX7NYjKq7Sd0qG7O	owner	2025-10-05 22:32:55.741149
15	19	dev+1759704037@example.com	$2b$12$GB1sVNVq1RfXWUGMui3.jemvygy6zsv2.mUhVZkycvQjqUkOlE.Se	owner	2025-10-05 22:40:37.466969
16	20	dev+1759704094@example.com	$2b$12$Aj5vC0hedrvHu5vNIwOX5eu7S2eRBZZLapxWOF4M.1Sy7npVnMcda	owner	2025-10-05 22:41:34.918484
17	21	dev+1759705285@example.com	$2b$12$A0uR7R06lAfPUFBe8n1OweQeBVgvRfe.GBIKqNraYdbiRPEMH807.	owner	2025-10-05 23:01:26.220606
\.


--
-- Name: blacklisted_tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mailforge_user
--

SELECT pg_catalog.setval('public.blacklisted_tokens_id_seq', 1, false);


--
-- Name: campaign_batches_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mailforge_user
--

SELECT pg_catalog.setval('public.campaign_batches_id_seq', 2, true);


--
-- Name: campaigns_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mailforge_user
--

SELECT pg_catalog.setval('public.campaigns_id_seq', 20, true);


--
-- Name: message_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mailforge_user
--

SELECT pg_catalog.setval('public.message_logs_id_seq', 1, true);


--
-- Name: password_reset_tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mailforge_user
--

SELECT pg_catalog.setval('public.password_reset_tokens_id_seq', 1, false);


--
-- Name: placement_results_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mailforge_user
--

SELECT pg_catalog.setval('public.placement_results_id_seq', 1, false);


--
-- Name: recipients_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mailforge_user
--

SELECT pg_catalog.setval('public.recipients_id_seq', 574, true);


--
-- Name: refresh_tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mailforge_user
--

SELECT pg_catalog.setval('public.refresh_tokens_id_seq', 82, true);


--
-- Name: seed_inboxes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mailforge_user
--

SELECT pg_catalog.setval('public.seed_inboxes_id_seq', 1, false);


--
-- Name: smtp_accounts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mailforge_user
--

SELECT pg_catalog.setval('public.smtp_accounts_id_seq', 12, true);


--
-- Name: suppressions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mailforge_user
--

SELECT pg_catalog.setval('public.suppressions_id_seq', 1, false);


--
-- Name: tenant_messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mailforge_user
--

SELECT pg_catalog.setval('public.tenant_messages_id_seq', 67, true);


--
-- Name: tenants_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mailforge_user
--

SELECT pg_catalog.setval('public.tenants_id_seq', 21, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mailforge_user
--

SELECT pg_catalog.setval('public.users_id_seq', 17, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: blacklisted_tokens blacklisted_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.blacklisted_tokens
    ADD CONSTRAINT blacklisted_tokens_pkey PRIMARY KEY (id);


--
-- Name: campaign_batches campaign_batches_pkey; Type: CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.campaign_batches
    ADD CONSTRAINT campaign_batches_pkey PRIMARY KEY (id);


--
-- Name: campaigns campaigns_pkey; Type: CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.campaigns
    ADD CONSTRAINT campaigns_pkey PRIMARY KEY (id);


--
-- Name: message_logs message_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.message_logs
    ADD CONSTRAINT message_logs_pkey PRIMARY KEY (id);


--
-- Name: password_reset_tokens password_reset_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_pkey PRIMARY KEY (id);


--
-- Name: placement_results placement_results_pkey; Type: CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.placement_results
    ADD CONSTRAINT placement_results_pkey PRIMARY KEY (id);


--
-- Name: recipients recipients_pkey; Type: CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.recipients
    ADD CONSTRAINT recipients_pkey PRIMARY KEY (id);


--
-- Name: refresh_tokens refresh_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_pkey PRIMARY KEY (id);


--
-- Name: seed_inboxes seed_inboxes_pkey; Type: CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.seed_inboxes
    ADD CONSTRAINT seed_inboxes_pkey PRIMARY KEY (id);


--
-- Name: smtp_accounts smtp_accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.smtp_accounts
    ADD CONSTRAINT smtp_accounts_pkey PRIMARY KEY (id);


--
-- Name: suppressions suppressions_pkey; Type: CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.suppressions
    ADD CONSTRAINT suppressions_pkey PRIMARY KEY (id);


--
-- Name: tenant_messages tenant_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.tenant_messages
    ADD CONSTRAINT tenant_messages_pkey PRIMARY KEY (id);


--
-- Name: tenants tenants_name_key; Type: CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.tenants
    ADD CONSTRAINT tenants_name_key UNIQUE (name);


--
-- Name: tenants tenants_pkey; Type: CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.tenants
    ADD CONSTRAINT tenants_pkey PRIMARY KEY (id);


--
-- Name: smtp_accounts uq_smtp_account; Type: CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.smtp_accounts
    ADD CONSTRAINT uq_smtp_account UNIQUE (tenant_id, host, port, username);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_blacklisted_tokens_token; Type: INDEX; Schema: public; Owner: mailforge_user
--

CREATE UNIQUE INDEX ix_blacklisted_tokens_token ON public.blacklisted_tokens USING btree (token);


--
-- Name: ix_message_logs_recipient; Type: INDEX; Schema: public; Owner: mailforge_user
--

CREATE INDEX ix_message_logs_recipient ON public.message_logs USING btree (recipient);


--
-- Name: ix_message_logs_tenant_id; Type: INDEX; Schema: public; Owner: mailforge_user
--

CREATE INDEX ix_message_logs_tenant_id ON public.message_logs USING btree (tenant_id);


--
-- Name: ix_password_reset_tokens_id; Type: INDEX; Schema: public; Owner: mailforge_user
--

CREATE INDEX ix_password_reset_tokens_id ON public.password_reset_tokens USING btree (id);


--
-- Name: ix_password_reset_tokens_user_id; Type: INDEX; Schema: public; Owner: mailforge_user
--

CREATE INDEX ix_password_reset_tokens_user_id ON public.password_reset_tokens USING btree (user_id);


--
-- Name: ix_recipients_email; Type: INDEX; Schema: public; Owner: mailforge_user
--

CREATE INDEX ix_recipients_email ON public.recipients USING btree (email);


--
-- Name: ix_refresh_tokens_id; Type: INDEX; Schema: public; Owner: mailforge_user
--

CREATE INDEX ix_refresh_tokens_id ON public.refresh_tokens USING btree (id);


--
-- Name: ix_refresh_tokens_user_id; Type: INDEX; Schema: public; Owner: mailforge_user
--

CREATE INDEX ix_refresh_tokens_user_id ON public.refresh_tokens USING btree (user_id);


--
-- Name: ix_suppressions_email; Type: INDEX; Schema: public; Owner: mailforge_user
--

CREATE INDEX ix_suppressions_email ON public.suppressions USING btree (email);


--
-- Name: campaign_batches campaign_batches_campaign_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.campaign_batches
    ADD CONSTRAINT campaign_batches_campaign_id_fkey FOREIGN KEY (campaign_id) REFERENCES public.campaigns(id) ON DELETE CASCADE;


--
-- Name: campaigns campaigns_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.campaigns
    ADD CONSTRAINT campaigns_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.tenants(id) ON DELETE CASCADE;


--
-- Name: password_reset_tokens password_reset_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: placement_results placement_results_campaign_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.placement_results
    ADD CONSTRAINT placement_results_campaign_id_fkey FOREIGN KEY (campaign_id) REFERENCES public.campaigns(id) ON DELETE CASCADE;


--
-- Name: recipients recipients_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.recipients
    ADD CONSTRAINT recipients_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.tenants(id) ON DELETE CASCADE;


--
-- Name: refresh_tokens refresh_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: seed_inboxes seed_inboxes_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.seed_inboxes
    ADD CONSTRAINT seed_inboxes_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.tenants(id) ON DELETE CASCADE;


--
-- Name: smtp_accounts smtp_accounts_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.smtp_accounts
    ADD CONSTRAINT smtp_accounts_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.tenants(id) ON DELETE CASCADE;


--
-- Name: suppressions suppressions_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.suppressions
    ADD CONSTRAINT suppressions_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.tenants(id) ON DELETE CASCADE;


--
-- Name: tenant_messages tenant_messages_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.tenant_messages
    ADD CONSTRAINT tenant_messages_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.tenants(id) ON DELETE CASCADE;


--
-- Name: users users_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mailforge_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.tenants(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict Yit6JLX3ZQprhRdJiBrXV8aSMg1nB29xCGTeYdKbEBgeFhtmcoeTB23qmMtJtTW

