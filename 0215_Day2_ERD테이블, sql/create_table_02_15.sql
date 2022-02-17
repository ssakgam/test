-- ======== drop table ===========

drop table follow;
drop table hash_tag_rel;
drop table hash_tag;

drop table post_file;
drop TABLE post;

drop table search_word;
drop table account;
 
drop table store_menu;
drop table store;  

-- ======== drop sequence ===========
drop sequence account_seq; 

drop sequence post_seq;
drop sequence post_f_seq;

drop sequence store_seq;
drop sequence store_m_seq; 

drop sequence follow_seq;
drop sequence search_word_seq;
drop sequence hash_tag_seq;
drop sequence hash_tag_rel_seq;

--------------------- 스토어 관리
create table store(
    id              number      constraint store_id_pk primary key,
    regist_date     date default sysdate,
    update_date     date default sysdate,
    name            varchar2(100)   constraint store_name_nn not null,
    address         varchar2(100)   constraint store_addr_nn not null,
    phone           varchar2(20),
    running_time    varchar2(50),
    soge            varchar2(200)
);
create sequence store_seq
increment by 1
start with 1;

create table store_menu(
    ID             number     constraint store_m_id_pk primary key,
    StoreID_FK     number     not null,
    m_name         varchar(20)    not null,
    price          number     not null,
    description    varchar2(100),
    constraint sm_storeid_fk foreign key(storeid_fk) references store(id) on delete cascade
);
create sequence store_m_seq
increment by 1
start with 1;




-------------------------- 회원 관리  수정본  --------------------------
CREATE TABLE account(
    id          number       CONSTRAINT account_id_pk PRIMARY KEY,
    user_id     VARCHAR2(20) CONSTRAINT user_id_un UNIQUE not null,
    pwd         VARCHAR2(20) not null,
    name        VARCHAR2(20) not null,
    acc         VARCHAR2(20) constraint user_acc_ck check(acc='admin' or acc='customer'),
    gender      CHAR(1) constraint gender_check check(gender in ('F','M')),
    age         NUMBER,
    email       VARCHAR2(50),
    reg_date    date DEFAULT sysdate,
    phone       varchar2(20) not null,
    address     VARCHAR2(100)
);
create sequence account_seq 
INCREMENT by 1
start with 1;

----------------- 리뷰글 관리
-- 리뷰 게시글
CREATE TABLE post(
    id              number CONSTRAINT post_id_PK PRIMARY KEY,
    storeId_fk      number,
    accId_fk   number,
    title           varchar2(100)    not null,
    content         VARCHAR2(2000)   not null,
    star_rate       number,
    register_date   date default sysdate not null, 
    update_date     date default sysdate not null,
    constraint post_storeId_fk foreign key(storeId_fk) references store(id) on delete cascade,
    constraint post_accId_fk foreign key(accId_fk) references account(id) on delete cascade
 );
create sequence post_seq
increment by 1
start with 1;





--============================================================
-- 게시글에 달린 첨부 파일
-- 다른 테이블에서 사용하기 위해, 컬럼명을 target_id로 변경
-- 걸려있던 fk 제약조건은 삭제하였습니다.
create table post_file(
   id           number CONSTRAINT post_file_id_PK PRIMARY KEY,
   target_name  CHAR(1) constraint post_file_ch check(target_name in ('c','s','p')),
   target_id    number,
   file_name    varchar2(40) not null,
   upload_path  varchar2(200) not null
);

create sequence post_f_seq
increment by 1
start with 1;


--============================================================
-- 검색어 테이블 
create table search_word(
     id number constraint search_word_id_pk primary key,
     word varchar2(100),
     accid number,
     search_time date DEFAULT sysdate,
     constraint sw_account_id_fk foreign key(accid)references account(id) on delete cascade
);

create sequence search_word_seq
increment by 1
start with 1;
--============================================================
-- 팔로우 
create table follow(
   id number constraint follow_id_pk primary key,
   target_name char(1) constraint follow_ch check(target_name in ('c','s','p')),
   target_id number,
   follower number
);

create sequence follow_seq
increment by 1
start with 1;

--============================================================
-- hash_tag table
-- food category인지, theme 카테고리인지 or 리뷰에 달린 아무런 문장, other hash tag인지..?
-- 아니면 뭐.. 긍/부..? 뭘 해야하지
create table hash_tag (
    id          number constraint hash_tag_id_pk primary key,
    category    varchar(20) constraint what_category_is check(category in ('menu', 'theme', 'rate')),
    tag_word    varchar(30)
);

create sequence hash_tag_seq
increment by 1
start with 1;


drop table hash_tag_rel

create table hash_tag_rel (
    id           number constraint hash_tag_rel_id_pk primary key,
    target_name  CHAR(1) constraint from_where_tag check(target_name in ('c', 's', 'p')),
    target_id    number, 
	hashtag_id 		 number, 
    --constraint tag_rel_tag_fk foreign key(target_id) references hash_tag(id) on delete cascade
	constraint tag_rel_tag_fk foreign key(hashtag_id) references hash_tag(id) on delete cascade
);





create sequence hash_tag_rel_seq
increment by 1
start with 1; 

