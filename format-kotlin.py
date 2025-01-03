import sublime, sublime_plugin
import subprocess

class FormatKotlinCommand(sublime_plugin.TextCommand):
  tmp_filepath = "/tmp/sublime-kotlin-format.kt"

  def execShell(self, command):
    proc = subprocess.Popen(
      command,
      shell=True,
      bufsize=-1,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      stdin=subprocess.PIPE,
    )
    return proc.communicate()

  def run(self, edit):
    fnamesplit = self.view.file_name().split('/')
    projectindex = fnamesplit.index("Projects") + 1
    configfname = '/'.join(fnamesplit[:projectindex + 1] + [".editorconfig"])
    region = sublime.Region(0, self.view.size())
    with open(self.tmp_filepath, 'w') as f:
      f.write(self.view.substr(region))
    output, error = self.execShell("ktlint -F --editorconfig=" + configfname + " " + self.tmp_filepath)
    if not error:
      with open(self.tmp_filepath, 'r') as f:
        self.view.replace(edit, region, f.read())

class AutoRunKotlinFormatOnSave(sublime_plugin.EventListener):
  def on_pre_save(self, view):
    file_path = view.file_name()
    if not file_path:
      return
    if file_path.split('.')[-1] != "kt":
      return
    view.run_command("format_kotlin")
