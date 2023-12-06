from flask import Blueprint,request, render_template,flash,redirect,url_for
from sqlalchemy import text
import matplotlib.font_manager as fm
from flask import Flask
import pandas as pd
import matplotlib.pyplot as plt
#一些可视化
from exts import engine
bp = Blueprint("view", __name__, url_prefix="/admin/view")
@bp.route('/user_order',methods=['GET','POST'])
def user_order():
    if request.method == 'GET':
        user_order_rank = text("""
        SELECT u.UserID,u.UserName,u.MusicName,us.OrderCount
        FROM userorder_view AS u,user_order_rankview AS us
        WHERE u.UserID = us.UserID
        ORDER BY       
            OrderCount DESC;
        """)
        with engine.connect() as conn:
            result = conn.execute(user_order_rank).fetchall()  # 执行sql
        # for row in result:
        #     print("UserID: ", row.UserID)
        #     print("UserName: ", row.UserName)
        #     print("MusicName: ", row.MusicName)
        #     print("OrderCount: ", row.OrderCount)
        #     print()
        return render_template('user-order-rank.html',result=result)
    else:
        user_id = request.form.get("userid")  # 要搜索用户id
        if user_id == '':
            flash("请输入数据")
            return redirect(url_for("view.user_order"))  # 当没有
        else:
            user_order_rank_search = text("""
                    SELECT u.UserID,u.UserName,u.MusicName,us.OrderCount
                    FROM userorder_view AS u,user_order_rankview AS us
                    WHERE u.UserID = us.UserID AND u.UserID =:userid;
                    """)
            with engine.connect() as conn:
                result_ = conn.execute(user_order_rank_search, {"userid": user_id}).fetchall()  # 执行sql
            if not result_:
                flash("不存在此用户")
                user_order_rank = text("""
                       SELECT u.UserID,u.UserName,u.MusicName,us.OrderCount
                       FROM userorder_view AS u,user_order_rankview AS us
                       WHERE u.UserID = us.UserID
                       ORDER BY       
                           OrderCount DESC;
                       """)
                with engine.connect() as conn:
                    result = conn.execute(user_order_rank).fetchall()  # 执行sql
                    return render_template('user-order-rank.html', result=result)
            else:
                return render_template('user-order-rank.html', result=result_)
@bp.route('/song_sales',methods=['GET','POST'])
def song_sales():
    if request.method == 'GET':
        song_sales = text("""
        SELECT s.MusicID,s.SongName,s.Singers,s.SalesCount,s.TotalRevenue
        FROM song_sales AS s
        ORDER BY       
            TotalRevenue DESC;
        """)
        with engine.connect() as conn:
            result = conn.execute(song_sales).fetchall()  # 执行sql
        return render_template('song-sales.html',result=result)
    else:
        music_name = request.form.get("musicname")  # 要搜索歌曲名字
        if music_name == '':
            flash("请输入数据")
            return redirect(url_for("view.song_sales"))  # 当没有
        else:
            song_sales_ = text("""
                    SELECT s.MusicID,s.SongName,s.Singers,s.SalesCount,s.TotalRevenue
                    FROM song_sales AS s
                    WHERE s.SongName =:music_name;
                    """)
            with engine.connect() as conn:
                result_ = conn.execute(song_sales_, {"music_name": music_name}).fetchall()  # 执行sql
            if not result_:
                flash("不存在此歌曲")
                song_sales = text("""
                SELECT s.MusicID,s.SongName,s.Singers,s.SalesCount,s.TotalRevenue
                FROM song_sales AS s
                ORDER BY       
                    TotalRevenue DESC;
                """)
                with engine.connect() as conn:
                    result = conn.execute(song_sales).fetchall()  # 执行sql
                    return render_template('song-sales.html', result=result)
            else:
                return render_template('song-sales.html', result=result_)

@bp.route('/weekly_sales')
def weekly_sales():
    weekly_sales_ = text("""
    SELECT *
    FROM weeklysales
    """)
    with engine.connect() as conn:
        result1 = conn.execute(weekly_sales_).fetchall()  # 执行sql
    # 获取前20项数据
    top_20_sales = result1[:20]
    df = pd.DataFrame(top_20_sales, columns=['Year', 'Week', 'TotalSongs', 'TotalAmount'])
    # 将'Year'和'Week'列转换为日期格式
    df['OrderTime'] = [f"{row[0]}-{row[1]}" for row in top_20_sales]
    df = df.sort_values('OrderTime')
    # 绘制销售总额的图表
    plt.figure(figsize=(12, 6))
    plt.plot(df['OrderTime'], df['TotalAmount'], marker='o', label='Total Amount')
    plt.xlabel('week')
    plt.ylabel('Total sales')
    plt.title('Weekly sales statistics')
    plt.xticks(rotation=45)  # 旋转x轴标签，避免重叠
    plt.legend()
    plt.savefig('./static/images/sales_total_amount.png')

    # 绘制销售数量的图表
    plt.figure(figsize=(12, 6))
    plt.plot(df['OrderTime'], df['TotalSongs'], marker='o', label='Songs Sold')
    plt.xlabel('week')
    plt.ylabel('Total number of songs sold')
    plt.title('Weekly sales statistics')
    plt.xticks(rotation=45)  # 旋转x轴标签，避免重叠
    plt.legend()
    plt.savefig('./static/images/sales_songs_sold.png')
    return render_template('weekly-sales.html',result1=result1)

@bp.route('/daily_sales')
def daily_sales():
    daily_sales_ = text("""
    SELECT *
    FROM daily_sales
    """)
    with engine.connect() as conn:
        result1 = conn.execute(daily_sales_).fetchall()  # 执行sql
    # 获取前20项数据
    top_20_sales = result1[:20]
    df = pd.DataFrame(top_20_sales, columns=['Date', 'TotalSongs', 'TotalAmount'])

    # 绘制销售总额的图表
    plt.figure(figsize=(14, 8))
    plt.plot(df['Date'], df['TotalAmount'], marker='o', label='Total Amount')
    plt.xlabel('Date')
    plt.ylabel('Total sales')
    plt.title('Daily sales statistics')
    plt.xticks(rotation=45)  # 旋转x轴标签，避免重叠
    plt.legend()
    plt.savefig('./static/images/daily_sales_amount.png')

    # 绘制销售数量的图表
    plt.figure(figsize=(14, 8))
    plt.plot(df['Date'], df['TotalSongs'], marker='o', label='Songs Sold')
    plt.xlabel('Date')
    plt.ylabel('Total number of songs sold')
    plt.title('Daily sales statistics')
    plt.xticks(rotation=45)  # 旋转x轴标签，避免重叠
    plt.legend()
    plt.savefig('./static/images/daily_sales_sold.png')
    return render_template('daily-sales.html',result1=result1)
