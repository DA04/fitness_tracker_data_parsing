PGDMP     %    8                z            garmin_data    13.6    13.6 !    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16394    garmin_data    DATABASE     o   CREATE DATABASE garmin_data WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'English_United States.1252';
    DROP DATABASE garmin_data;
                postgres    false            �            1259    16403    activity    TABLE     `  CREATE TABLE public.activity (
    activity_id bigint NOT NULL,
    "timestamp" timestamp with time zone,
    total_timer_time real,
    local_timestamp timestamp without time zone,
    num_sessions integer,
    type character varying(50),
    event character varying(50),
    event_type character varying(50),
    event_group character varying(50)
);
    DROP TABLE public.activity;
       public         heap    postgres    false            �            1259    16434    file_id    TABLE       CREATE TABLE public.file_id (
    file_id integer NOT NULL,
    serial_number bigint,
    tine_created real,
    manufacturer character varying(50),
    number real,
    type character varying(50),
    activity_id bigint NOT NULL,
    product character varying(50)
);
    DROP TABLE public.file_id;
       public         heap    postgres    false            �            1259    16432    file_id_record_id_seq    SEQUENCE     �   CREATE SEQUENCE public.file_id_record_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.file_id_record_id_seq;
       public          postgres    false    206            �           0    0    file_id_record_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.file_id_record_id_seq OWNED BY public.file_id.file_id;
          public          postgres    false    205            �            1259    16397    lap    TABLE       CREATE TABLE public.lap (
    lap_id integer NOT NULL,
    start_time timestamp with time zone,
    total_distance real,
    total_elapsed_time real,
    max_speed real,
    max_heart_rate smallint,
    avg_heart_rate smallint,
    activity_id bigint NOT NULL,
    number smallint
);
    DROP TABLE public.lap;
       public         heap    postgres    false            �            1259    16395    lap_record_id_seq    SEQUENCE     �   CREATE SEQUENCE public.lap_record_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.lap_record_id_seq;
       public          postgres    false    201            �           0    0    lap_record_id_seq    SEQUENCE OWNED BY     D   ALTER SEQUENCE public.lap_record_id_seq OWNED BY public.lap.lap_id;
          public          postgres    false    200            �            1259    16415    record    TABLE     m  CREATE TABLE public.record (
    record_id bigint NOT NULL,
    latitude double precision,
    longitude double precision,
    lap smallint,
    altitude real,
    "timestamp" timestamp with time zone,
    heart_rate smallint,
    cadence smallint,
    speed real,
    activity_id bigint NOT NULL,
    distance real,
    power smallint,
    temperature smallint
);
    DROP TABLE public.record;
       public         heap    postgres    false            �            1259    16413    record_record_id_seq    SEQUENCE     }   CREATE SEQUENCE public.record_record_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 +   DROP SEQUENCE public.record_record_id_seq;
       public          postgres    false    204            �           0    0    record_record_id_seq    SEQUENCE OWNED BY     M   ALTER SEQUENCE public.record_record_id_seq OWNED BY public.record.record_id;
          public          postgres    false    203            �            1259    16468    session    TABLE     T  CREATE TABLE public.session (
    session_id integer NOT NULL,
    activity_id bigint NOT NULL,
    "timestamp" timestamp with time zone,
    start_time timestamp with time zone,
    start_position_lat integer,
    start_position_long integer,
    total_elapsed_time real,
    total_timer_time real,
    total_distance real,
    total_strokes real,
    nec_lat integer,
    nec_long integer,
    swc_lat integer,
    swc_long integer,
    message_index integer,
    total_calories smallint,
    total_fat_calories real,
    enhanced_avg_speed real,
    avg_speed real,
    enhanced_max_speed real,
    max_speed real,
    avg_power real,
    max_power real,
    total_ascent smallint,
    total_descent smallint,
    first_lap_index smallint,
    num_laps smallint,
    event character varying(50),
    event_type character varying(50),
    sport character varying(50),
    sub_sport character varying(50),
    avg_heart_rate smallint,
    max_heart_rate smallint,
    avg_cadence smallint,
    max_cadence smallint,
    total_training_effect real,
    event_group real,
    trigger character varying(50)
);
    DROP TABLE public.session;
       public         heap    postgres    false            �            1259    16466    session_session_id_seq    SEQUENCE     �   CREATE SEQUENCE public.session_session_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.session_session_id_seq;
       public          postgres    false    208            �           0    0    session_session_id_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.session_session_id_seq OWNED BY public.session.session_id;
          public          postgres    false    207            �            1259    24635    test    TABLE     �   CREATE TABLE public.test (
    test_id integer DEFAULT nextval('public.session_session_id_seq'::regclass) NOT NULL,
    activity_id bigint NOT NULL,
    power_threshold smallint,
    test_type character(25),
    "timestamp" timestamp with time zone
);
    DROP TABLE public.test;
       public         heap    postgres    false    207            ?           2604    16437    file_id file_id    DEFAULT     t   ALTER TABLE ONLY public.file_id ALTER COLUMN file_id SET DEFAULT nextval('public.file_id_record_id_seq'::regclass);
 >   ALTER TABLE public.file_id ALTER COLUMN file_id DROP DEFAULT;
       public          postgres    false    205    206    206            =           2604    16400 
   lap lap_id    DEFAULT     k   ALTER TABLE ONLY public.lap ALTER COLUMN lap_id SET DEFAULT nextval('public.lap_record_id_seq'::regclass);
 9   ALTER TABLE public.lap ALTER COLUMN lap_id DROP DEFAULT;
       public          postgres    false    200    201    201            >           2604    16418    record record_id    DEFAULT     t   ALTER TABLE ONLY public.record ALTER COLUMN record_id SET DEFAULT nextval('public.record_record_id_seq'::regclass);
 ?   ALTER TABLE public.record ALTER COLUMN record_id DROP DEFAULT;
       public          postgres    false    203    204    204            @           2604    16471    session session_id    DEFAULT     x   ALTER TABLE ONLY public.session ALTER COLUMN session_id SET DEFAULT nextval('public.session_session_id_seq'::regclass);
 A   ALTER TABLE public.session ALTER COLUMN session_id DROP DEFAULT;
       public          postgres    false    208    207    208            E           2606    16407    activity activity_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public.activity
    ADD CONSTRAINT activity_pkey PRIMARY KEY (activity_id);
 @   ALTER TABLE ONLY public.activity DROP CONSTRAINT activity_pkey;
       public            postgres    false    202            I           2606    16439    file_id file_id_pk 
   CONSTRAINT     U   ALTER TABLE ONLY public.file_id
    ADD CONSTRAINT file_id_pk PRIMARY KEY (file_id);
 <   ALTER TABLE ONLY public.file_id DROP CONSTRAINT file_id_pk;
       public            postgres    false    206            C           2606    16402    lap record_id_pk 
   CONSTRAINT     R   ALTER TABLE ONLY public.lap
    ADD CONSTRAINT record_id_pk PRIMARY KEY (lap_id);
 :   ALTER TABLE ONLY public.lap DROP CONSTRAINT record_id_pk;
       public            postgres    false    201            G           2606    16420    record records_pk 
   CONSTRAINT     V   ALTER TABLE ONLY public.record
    ADD CONSTRAINT records_pk PRIMARY KEY (record_id);
 ;   ALTER TABLE ONLY public.record DROP CONSTRAINT records_pk;
       public            postgres    false    204            K           2606    16473    session session_pk 
   CONSTRAINT     X   ALTER TABLE ONLY public.session
    ADD CONSTRAINT session_pk PRIMARY KEY (session_id);
 <   ALTER TABLE ONLY public.session DROP CONSTRAINT session_pk;
       public            postgres    false    208            M           2606    24640    test test_pk 
   CONSTRAINT     O   ALTER TABLE ONLY public.test
    ADD CONSTRAINT test_pk PRIMARY KEY (test_id);
 6   ALTER TABLE ONLY public.test DROP CONSTRAINT test_pk;
       public            postgres    false    209            N           2606    16408    lap activity_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.lap
    ADD CONSTRAINT activity_fk FOREIGN KEY (activity_id) REFERENCES public.activity(activity_id) NOT VALID;
 9   ALTER TABLE ONLY public.lap DROP CONSTRAINT activity_fk;
       public          postgres    false    201    2885    202            O           2606    16421    record activity_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.record
    ADD CONSTRAINT activity_fk FOREIGN KEY (activity_id) REFERENCES public.activity(activity_id);
 <   ALTER TABLE ONLY public.record DROP CONSTRAINT activity_fk;
       public          postgres    false    202    2885    204            Q           2606    16474    session activity_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.session
    ADD CONSTRAINT activity_fk FOREIGN KEY (activity_id) REFERENCES public.activity(activity_id);
 =   ALTER TABLE ONLY public.session DROP CONSTRAINT activity_fk;
       public          postgres    false    202    2885    208            P           2606    16440    file_id activity_id_fk    FK CONSTRAINT     �   ALTER TABLE ONLY public.file_id
    ADD CONSTRAINT activity_id_fk FOREIGN KEY (activity_id) REFERENCES public.activity(activity_id);
 @   ALTER TABLE ONLY public.file_id DROP CONSTRAINT activity_id_fk;
       public          postgres    false    2885    206    202            R           2606    24641    test fk_activity_id    FK CONSTRAINT     �   ALTER TABLE ONLY public.test
    ADD CONSTRAINT fk_activity_id FOREIGN KEY (activity_id) REFERENCES public.activity(activity_id);
 =   ALTER TABLE ONLY public.test DROP CONSTRAINT fk_activity_id;
       public          postgres    false    2885    209    202           