from flask import Blueprint, request, jsonify, g
from app.routes.auth import token_required
from app.models import db, SysOperLog, SysLoginLog

bp = Blueprint('logs', __name__)


@bp.route('/oper', methods=['GET'])
@token_required
def get_oper_logs():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    title = request.args.get('title', '')
    oper_name = request.args.get('operName', '')
    status = request.args.get('status', type=int)
    start_time = request.args.get('startTime', '')
    end_time = request.args.get('endTime', '')

    query = SysOperLog.query

    if title:
        query = query.filter(SysOperLog.title.like(f'%{title}%'))
    if oper_name:
        query = query.filter(SysOperLog.oper_name.like(f'%{oper_name}%'))
    if status is not None:
        query = query.filter(SysOperLog.status == status)
    if start_time:
        query = query.filter(SysOperLog.oper_time >= start_time)
    if end_time:
        query = query.filter(SysOperLog.oper_time <= end_time)

    total = query.count()
    logs = query.order_by(SysOperLog.oper_time.desc()).offset((page - 1) * page_size).limit(page_size).all()

    log_list = []
    for log in logs:
        log_list.append({
            'operId': log.oper_id,
            'title': log.title,
            'businessType': log.business_type,
            'method': log.method,
            'operName': log.oper_name,
            'operUrl': log.oper_url,
            'operIp': log.oper_ip,
            'operTime': log.oper_time.strftime('%Y-%m-%d %H:%M:%S') if log.oper_time else None,
            'status': log.status,
            'costTime': log.cost_time
        })

    return jsonify({'code': 200, 'msg': 'success', 'data': {'list': log_list, 'total': total, 'page': page, 'pageSize': page_size}})


@bp.route('/login', methods=['GET'])
@token_required
def get_login_logs():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    user_name = request.args.get('userName', '')
    status = request.args.get('status', '')
    start_time = request.args.get('startTime', '')
    end_time = request.args.get('endTime', '')

    query = SysLoginLog.query

    if user_name:
        query = query.filter(SysLoginLog.user_name.like(f'%{user_name}%'))
    if status:
        query = query.filter(SysLoginLog.status == status)
    if start_time:
        query = query.filter(SysLoginLog.login_time >= start_time)
    if end_time:
        query = query.filter(SysLoginLog.login_time <= end_time)

    total = query.count()
    logs = query.order_by(SysLoginLog.login_time.desc()).offset((page - 1) * page_size).limit(page_size).all()

    log_list = []
    for log in logs:
        log_list.append({
            'infoId': log.info_id,
            'userName': log.user_name,
            'ipaddr': log.ipaddr,
            'loginLocation': log.login_location,
            'browser': log.browser,
            'os': log.os,
            'status': log.status,
            'msg': log.msg,
            'loginTime': log.login_time.strftime('%Y-%m-%d %H:%M:%S') if log.login_time else None
        })

    return jsonify({'code': 200, 'msg': 'success', 'data': {'list': log_list, 'total': total, 'page': page, 'pageSize': page_size}})
