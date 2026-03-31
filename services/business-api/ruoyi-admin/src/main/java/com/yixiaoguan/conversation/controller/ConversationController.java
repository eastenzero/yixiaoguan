package com.yixiaoguan.conversation.controller;

import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.utils.SecurityUtils;
import com.yixiaoguan.common.core.domain.YxUser;
import com.yixiaoguan.conversation.domain.YxConversation;
import com.yixiaoguan.conversation.domain.YxMessage;
import com.yixiaoguan.conversation.service.IYxConversationService;
import com.yixiaoguan.conversation.service.IYxMessageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * 会话 Controller
 * 路由前缀：/api/v1/conversations
 */
@RestController
@RequestMapping("/api/v1/conversations")
public class ConversationController {

    @Autowired
    private IYxConversationService conversationService;

    @Autowired
    private IYxMessageService messageService;

    /**
     * 获取当前登录学生的会话列表（分页）
     * GET /api/v1/conversations?status=1&pageNum=1&pageSize=10
     */
    @GetMapping
    public AjaxResult listMyConversations(
            @RequestParam(required = false) Integer status,
            @RequestParam(defaultValue = "1") int pageNum,
            @RequestParam(defaultValue = "10") int pageSize) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        Map<String, Object> result = conversationService.selectPageByUserId(
                currentUser.getId(), status, pageNum, pageSize);
        return AjaxResult.success(result);
    }

    /**
     * 获取指定会话详情
     * GET /api/v1/conversations/{id}
     */
    @GetMapping("/{id}")
    public AjaxResult getConversation(@PathVariable Long id) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        YxConversation conversation = conversationService.selectById(id, currentUser.getId());
        return AjaxResult.success(conversation);
    }

    /**
     * 新建会话（学生发起提问会话）
     * POST /api/v1/conversations
     * Body: { "title": "xxx" }  // title 可为空
     */
    @PostMapping
    public AjaxResult createConversation(@RequestBody(required = false) Map<String, String> body) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        String title = (body != null) ? body.get("title") : null;
        YxConversation conversation = conversationService.createConversation(currentUser.getId(), title);
        return AjaxResult.success(conversation);
    }

    /**
     * 更新会话标题
     * PUT /api/v1/conversations/{id}/title
     * Body: { "title": "新标题" }
     */
    @PutMapping("/{id}/title")
    public AjaxResult updateTitle(@PathVariable Long id,
                                   @RequestBody Map<String, String> body) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        String title = body.get("title");
        conversationService.updateTitle(id, currentUser.getId(), title);
        return AjaxResult.success();
    }

    /**
     * 关闭会话（软删除）
     * DELETE /api/v1/conversations/{id}
     */
    @DeleteMapping("/{id}")
    public AjaxResult closeConversation(@PathVariable Long id) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        conversationService.closeConversation(id, currentUser.getId());
        return AjaxResult.success();
    }

    /**
     * 获取会话的全量历史消息（适用于初次加载）
     * GET /api/v1/conversations/{id}/messages
     */
    @GetMapping("/{id}/messages")
    public AjaxResult getHistory(@PathVariable Long id) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        // 先做会话归属校验
        conversationService.selectById(id, currentUser.getId());
        return AjaxResult.success(messageService.selectHistory(id, currentUser.getId()));
    }

    /**
     * 分页获取历史消息（翻页场景）
     * GET /api/v1/conversations/{id}/messages/page?pageNum=1&pageSize=20
     */
    @GetMapping("/{id}/messages/page")
    public AjaxResult getMessagePage(
            @PathVariable Long id,
            @RequestParam(defaultValue = "1") int pageNum,
            @RequestParam(defaultValue = "20") int pageSize) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        conversationService.selectById(id, currentUser.getId());
        Map<String, Object> result = messageService.selectPage(id, pageNum, pageSize);
        return AjaxResult.success(result);
    }

    /**
     * 学生/教师在会话内发送消息（HTTP 方式，WebSocket 上行走另一个通道）
     * POST /api/v1/conversations/{id}/messages
     * Body: { "content": "xxx", "messageType": 1, "parentMessageId": null }
     */
    @PostMapping("/{id}/messages")
    public AjaxResult sendMessage(@PathVariable Long id,
                                   @RequestBody Map<String, Object> body) {
        YxUser currentUser = SecurityUtils.getLoginUser().getYxUser();
        // 校验会话归属（学生只能在自己的会话中发，教师需已介入）
        YxConversation conversation = conversationService.selectById(id, currentUser.getId());

        YxMessage message = new YxMessage();
        message.setConversationId(id);
        // 根据角色判断 sender_type（业务层简化：登录用户自己发的消息，由 Controller 填充角色）
        // 教师介入时 status=2，否则默认为学生
        if (Integer.valueOf(2).equals(conversation.getStatus())
                && currentUser.getId().equals(conversation.getTeacherId())) {
            message.setSenderType(3); // 3-教师
        } else {
            message.setSenderType(1); // 1-学生
        }
        message.setSenderId(currentUser.getId());
        message.setContent((String) body.get("content"));
        Object mt = body.get("messageType");
        message.setMessageType(mt != null ? ((Number) mt).intValue() : 1);
        Object pmid = body.get("parentMessageId");
        message.setParentMessageId(pmid != null ? Long.parseLong(pmid.toString()) : null);

        YxMessage saved = messageService.sendMessage(message);
        return AjaxResult.success(saved);
    }
}
