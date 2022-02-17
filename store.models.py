
# 가게 목록 출력 version1
# 검색기능 구현 전 만든 가게목록용 함수입니다. 지금은 사용하지 않지만 참고용으로 남겨두었습니다.
# 현재는 검색 결과에 따른 가게목록을 출력해주는 하단의 search_by_name 함수를 사용합니다.
def storelist():
    conn = ora.connect(database)   # oracle 접속
    cursor = conn.cursor()   # cursor == PreparedeStatement
    sql ='''   select s.id, s.name, fc.name, s.address, s.running_time
                from store s, food_category fc, category c
                where fc.id = c.foodid_fk 
                and c.storeid_fk = s.id 
    '''
    cursor.execute(sql)
    res = cursor.fetchall()
    # count = cursor.fetchall().count()
    # print(count)
    cursor.close()
    conn.close()
    return res

# 가게 목록 출력 version2
# 상호명이나 메뉴에 검색어가 포함 된 가게 검색
# order는 검색창 왼쪽의 select 선택 결과 (최신,오래된,평점낮은,평점높은순)
def search_by_name(search_value, order):
    conn = ora.connect(database)
    cursor = conn.cursor()
    # select (가게ID, 상호명, 가게주소, 운영시간, 평점, 대문사진파일명, 파일경로)
    # 사진정보와, 평점 정보가 없는 가게도 나와야 하므로 full outer join을 사용하였습니다.
    # 가게 평점의 경우 소수점 1자리까지 나오고, 리뷰글이 없는 가게의 경우 0점으로 나오도록 설정하였습니다.
    sql = '''select s.id, s.name, s.address, s.running_time,DECODE(p.s_avg, null, 0, p.s_avg) avg, pf.file_name, pf.upload_path
            from store s
            full outer join post_file pf
            on s.id = pf.target_id
                full outer join (select p.storeid_fk sfk, round(avg(p.star_rate),1) s_avg
                                    from store s, post p
                                    where s.id = p.storeid_fk 
                                    group by p.storeid_fk) p
                on s.id = p.sfk 
            where s.name in(select s.name
                            from store s, store_menu sm
                            where s.id = sm.storeid_fk
                            and sm.m_name like '%'||:a||'%'
                            or s.name like '%'||:a||'%') 

'''
    #하단의 조건문은 사용자가 선택한 정렬조건에 따라 위의 sql문에 order by 절을 추가합니다.
    if order == 'new':
        sql = sql + 'order by s.id desc'
    elif order =='old':
        sql = sql + 'order by s.id asc'
    elif order =='star_desc':
        sql = sql + 'order by avg desc'
    elif order =='star_asc':
        sql = sql + 'order by avg asc'
    else:
        sql = sql + 'order by s.id desc'

    cursor.execute(sql, a=search_value)
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res

# param -> 가게 id
# 가게 디테일 화면에 띄워줄 정보를 가져오는 함수입니다.
def store_detail(s_id):
    conn = ora.connect(database)
    cursor = conn.cursor()
    # select ( 가게id, 상호명, 전화번호, 주소, 영업시간, 소개글 )
    sql ='''select s.id, s.name, fc.name, s.phone, s.address, s.running_time, s.soge
            from store s, food_category fc, category c
            where fc.id = c.foodid_fk 
            and c.storeid_fk = s.id 
            and s.id=:id
    '''
    cursor.execute(sql, id=s_id)
    detail = cursor.fetchone()
    cursor.close()
    conn.close()
    return detail

# param -> 가게 id
# 해당 가게에서 판매하는 메뉴 정보를 가져오는 함수입니다.
def store_menu(s_id):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql ='''select sm.id, sm.m_name, sm.price, sm.description
            from store s, store_menu sm
            where s.id = sm.storeid_fk
            and s.id=:id
    '''
    cursor.execute(sql, id=s_id)
    menu = cursor.fetchall()
    cursor.close()
    conn.close()
    return menu

# param -> 가게 id
# 헤당 가게에 달린 게시글 목록 출력
def store_post_list(s_id):
    conn = ora.connect(database)
    cursor = conn.cursor()
    # select ( 게시글id, 제목, 내용, 별점, 수정일 )
    # 별점 출력의 경우 LPAD를 사용하였지만, substr('*****',0,star_rate)를 사용하여도 무방합니다.
    sql ='''select p.id, p.title, p.content, LPAD('⭐⭐⭐⭐⭐',p.star_rate,'⭐'), p.update_date
            from store s, post p
            where s.id = p.storeid_fk
            and s.id=:id
    '''
    cursor.execute(sql, id=s_id)
    post_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return post_list

# 가게별 평점(가게id)
# 초기에 가게별 평점을 구하기 위해 작성하였지만, search_by_name함수에서 함께 처리하기로 변경되어서,
# 지금은 사용하지 않습니다. 학습용으로 남겨두겠습니다.
def store_star_avg(s_id):
    conn = ora.connect(database)
    cursor = conn.cursor()
    sql ='''select avg(p.star_rate)
            from store s, post p
            where s.id = p.storeid_fk 
            group by p.storeid_fk
            having p.storeid_fk =:id
            '''
    cursor.execute(sql, id=s_id)
    s_star_rate = cursor.fetchone()
    cursor.close()
    conn.close()
    return s_star_rate

# 가게 이미지파일 정보 가져오기
def get_image_data(idx):
    conn = ora.connect(database)
    cursor = conn.cursor()
    # select( 업로드경로, 사진파일명 )
    # 다른 파트의 사진을 가져오는 경우를 방지하기 위해 target_name='s'조건을 추가하였습니다.
    sql = """
        select upload_path, file_name
          from post_file
         where target_id = :id
           and target_name = 's'
    """
    cursor.execute(sql, id=idx)
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    return res

# 파일이름 찾기
def get_file_name(idx):
    conn = ora.connect(database)
    cursor = conn.cursor()

    # 사진 이름 가져오기
    sql = '''
        select upload_path ,file_name
        from post_file
        where target_id=:id
    '''
    cursor.execute(sql, id=idx)
    res = cursor.fetchone()
    cursor.close()
    conn.commit()
    conn.close()
    return res

# 가게 삭제
def delete_store(idx):
    conn = ora.connect(database)
    cursor = conn.cursor()

    # 가게정보 삭제
    sql = "delete from store where id=:id"
    cursor.execute(sql, id=idx)

    # 가게 대문사진 파일 정보 삭제
    sql = "delete from post_file where target_id=:id and target_name = 's' "
    cursor.execute(sql, id=idx)

    cursor.close()
    conn.commit()
    conn.close()

