// 模拟前端下载模板的测试
const axios = require('axios');
const fs = require('fs');

async function testDownload() {
    console.log('=== 测试下载模板功能 ===');
    
    try {
        // 1. 登录获取token
        console.log('1. 登录...');
        const loginRes = await axios.post('http://localhost:5000/api/auth/login', {
            username: 'admin',
            password: '123456'
        });
        const token = loginRes.data.data.token;
        console.log('登录成功，Token:', token.slice(0, 30) + '...');
        
        // 2. 下载模板（模拟前端请求）
        console.log('\n2. 下载模板...');
        const downloadRes = await axios.get('http://localhost:5000/api/publish/templates/download', {
            headers: {
                'Authorization': 'Bearer ' + token
            },
            responseType: 'blob'  // 关键：指定响应类型为blob
        });
        
        console.log('响应状态:', downloadRes.status);
        console.log('Content-Type:', downloadRes.headers['content-type']);
        console.log('Content-Disposition:', downloadRes.headers['content-disposition']);
        console.log('文件大小:', downloadRes.data.length, 'bytes');
        
        // 3. 保存到本地验证
        console.log('\n3. 保存文件到本地...');
        fs.writeFileSync('test_template.xlsx', downloadRes.data);
        console.log('文件保存成功！');
        
        // 4. 验证文件格式
        const fileBuffer = fs.readFileSync('test_template.xlsx');
        const magic = fileBuffer.slice(0, 4).toString('hex');
        console.log('文件头:', magic);
        if (magic === '504b0304') {  // ZIP格式（xlsx是zip压缩）
            console.log('✓ 文件格式正确（ZIP格式，xlsx文件）');
        } else {
            console.log('✗ 文件格式不正确');
        }
        
        console.log('\n=== 测试完成 ===');
        
    } catch (error) {
        console.error('测试失败:', error.message);
        if (error.response) {
            console.error('响应状态:', error.response.status);
            console.error('响应数据:', error.response.data);
        }
    }
}

testDownload();
