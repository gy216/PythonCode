import time
import sys

print('果园工作室-制作')
print('由群内的awa制作，果园允许改编','作者已给版权')
print('——————————————————————————————————————————————————————————————')

try:
    import requests
    print('requests库已导入')
    
    # 添加明确的退出确认
    site = 'https://gybc.top/home/'
    print(f'目标网址: {site}')
    confirm = input('确认要进行访问测试吗？(y/n): ')
    if confirm.lower() != 'y':
        sys.exit('用户取消操作')
    
    frequency = int(input('你要测试的次数: '))
    
    # 添加合理性检查
    if frequency <= 0:
        print('次数必须大于0')
        sys.exit(1)
    if frequency > 100:  # 限制最大次数
        print('次数过多，已限制为100次')
        frequency = 100
    
    print('请等待...')
    time.sleep(1)
    
    # 添加合理的请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print('开始测试...')
    print('_' * 60)
    
    success_count = 0
    failed_count = 0
    
    for i in range(frequency):
        try:
            response = requests.get(site, headers=headers, timeout=5)
            
            if response.status_code == 200:
                success_count += 1
                print(f'第{i+1}次: 成功 (状态码: {response.status_code})')
            else:
                failed_count += 1
                print(f'第{i+1}次: 失败 (状态码: {response.status_code})')
            
            # 添加适当延迟
            if i < frequency - 1:
                time.sleep(0.5)  # 0.5秒延迟
            
        except requests.exceptions.RequestException as e:
            failed_count += 1
            print(f'第{i+1}次: 请求异常 - {str(e)[:50]}')
            time.sleep(1)
    
    print('_' * 60)
    print(f'测试完成！')
    print(f'总次数: {frequency}, 成功: {success_count}, 失败: {failed_count}')
    print(f'成功率: {success_count/frequency*100:.1f}%' if frequency > 0 else '无测试')
    
except ImportError:
    print('未安装requests库，请执行: pip install requests')
except ValueError:
    print('请输入有效的数字')
except KeyboardInterrupt:
    print('\n用户中断操作')
except Exception as e:
    print(f'发生错误: {type(e).__name__} - {str(e)}')
