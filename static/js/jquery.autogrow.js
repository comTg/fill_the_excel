(function ($) {
    $.fn.autogrow = function (options) {
        var defaults = {
            minHeight: 0,
            maxHeight: 999
        };

        var options = $.extend(defaults, options);

        return this.each(function () {
            var element = $(this);
            //上一次文本框内容长度和宽度
            var lastValLength, lastWidth;
            //文本框内容长度、宽度和高度
            var valLength, width, height;

            //验证页面元素是textarea
            if (!element.is('textarea')) {
                return;
            }
            function set_height(node) {
                node.height(40);
                valLength = node.val().length;
                if(valLength>10){
                  height = Math.max(options.minHeight, Math.min(node.prop('scrollHeight'), options.maxHeight));
                //如果当前文本框的高度超过我们允许的最大高度的时候，隐藏多余文字；否则设置为auto
                //$(this).prop('scrollHeight') > height 只有在height取得的值是options.maxHeight才有意义
                node.css('overflow', (node.prop('scrollHeight') > height ? 'auto' : 'hidden'))
                    .height(height); //设置文本框高度
                }
            }
            element.css('overflow', 'hidden')
                .keydown(function () {   // 设置键盘按下事件                    //获取文本框内容长度
                    //我这里使用的jquery版本是1.8，获取css属性的方法已经变成了prop
                    //如果使用1.6以下版本的jquery，以下代码要变为 width = $(this).attr('offsetWidth');
                    //$(this).prop('scrollHeight')也要变为：$(this).attr('scrollHeight')
                    width = $(this).prop('offsetWidth');
                    //计算适合的文本框高度
                    set_height($(this));
                    lastValLength = valLength;
                    lastWidth = width;
                });
            element.blur(function () {
                $(this).height(40);
            });
            element.focus(function(){
                set_height($(this));
            });
        });
    }
})(jQuery);